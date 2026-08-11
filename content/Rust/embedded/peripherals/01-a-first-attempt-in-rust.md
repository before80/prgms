+++
title = "01-用 Rust 的第一次尝试"
date = 2026-08-01T10:38:00+08:00
weight = 56
type = "docs"
description = "用 Rust 的第一次尝试（A first attempt in Rust）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 用 Rust 的第一次尝试 {#a-first-attempt}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/peripherals/a-first-attempt.html](https://doc.rust-lang.org/stable/embedded-book/peripherals/a-first-attempt.html)


## 寄存器 {#the-registers}

我们来看一下「SysTick」外设 —— 每个 Cortex-M 处理器核都自带的一个简单定时器。通常你会在芯片厂商的数据手册或*技术参考手册（Technical Reference Manual）*里查找这些内容，但这个例子对所有 ARM Cortex-M 核都通用，我们来看 [ARM reference manual]。可以看到有四个寄存器：

[ARM reference manual]: http://infocenter.arm.com/help/topic/com.arm.doc.dui0553a/Babieigh.html

| 偏移   | 名称        | 描述                        | 宽度   |
|--------|-------------|-----------------------------|--------|
| 0x00   | SYST_CSR    | 控制和状态寄存器            | 32 位  |
| 0x04   | SYST_RVR    | 重载值寄存器                | 32 位  |
| 0x08   | SYST_CVR    | 当前值寄存器                | 32 位  |
| 0x0C   | SYST_CALIB  | 校准值寄存器                | 32 位  |

## C 风格的做法 {#the-c-approach}

在 Rust 中，我们可以用与 C 完全相同的方式表示一组寄存器 —— 用 `struct`。

```rust,ignore
#[repr(C)]
struct SysTick {
    pub csr: u32,
    pub rvr: u32,
    pub cvr: u32,
    pub calib: u32,
}
```

限定符 `#[repr(C)]` 告诉 Rust 编译器按 C 编译器的方式排布该结构体。这非常重要，因为 Rust 允许重新排列结构体字段，而 C 不允许。你可以想象，如果这些字段被编译器悄悄重排，调试会有多痛苦！加上这个限定符后，我们就有了与上表对应的四个 32 位字段。但当然，这个 `struct` 本身没什么用 —— 我们还需要一个变量。

```rust,ignore
let systick = 0xE000_E010 as *mut SysTick;
let time = unsafe { (*systick).cvr };
```

## 易失访问 {#volatile-accesses}

不过，上面的做法有几个问题。

1. 每次想访问外设时都必须使用 `unsafe`。
2. 我们无法指定哪些寄存器是只读或读写的。
3. 程序中任何地方的任何代码都可以通过这个结构体访问硬件。
4. 最重要的是，它实际上并不能正常工作……

问题在于编译器很聪明。如果你对同一块 RAM 连续写两次，编译器可能注意到这一点并完全跳过第一次写入。在 C 中，我们可以把变量标为 `volatile`，以确保每次读写都按预期发生。在 Rust 中，我们把*访问*标为易失（volatile），而不是变量本身。

```rust,ignore
let systick = unsafe { &mut *(0xE000_E010 as *mut SysTick) };
let time = unsafe { core::ptr::read_volatile(&mut systick.cvr) };
```

这样，四个问题里我们解决了一个，但现在 `unsafe` 代码更多了！幸好有一个第三方 crate 可以帮忙 —— [`volatile_register`]。

[`volatile_register`]: https://crates.io/crates/volatile_register

```rust,ignore
use volatile_register::{RW, RO};

#[repr(C)]
struct SysTick {
    pub csr: RW<u32>,
    pub rvr: RW<u32>,
    pub cvr: RW<u32>,
    pub calib: RO<u32>,
}

fn get_systick() -> &'static mut SysTick {
    unsafe { &mut *(0xE000_E010 as *mut SysTick) }
}

fn get_time() -> u32 {
    let systick = get_systick();
    systick.cvr.read()
}
```

现在，易失访问会通过 `read` 和 `write` 方法自动完成。执行写操作仍然是 `unsafe` 的，但公平地说，硬件本身就是一大堆可变状态，编译器无法知道这些写入是否真正安全，所以这是一个合理的默认立场。

## 更 Rust 风格的封装 {#the-rusty-wrapper}

我们需要把这个 `struct` 封装成更高层的 API，让用户可以安全调用。作为驱动作者，我们手动验证 `unsafe` 代码正确，然后向用户提供安全 API，让他们不必操心（前提是他们信任我们做对了！）。

一个例子可能是：

```rust,ignore
use volatile_register::{RW, RO};

pub struct SystemTimer {
    p: &'static mut RegisterBlock
}

#[repr(C)]
struct RegisterBlock {
    pub csr: RW<u32>,
    pub rvr: RW<u32>,
    pub cvr: RW<u32>,
    pub calib: RO<u32>,
}

impl SystemTimer {
    pub fn new() -> SystemTimer {
        SystemTimer {
            p: unsafe { &mut *(0xE000_E010 as *mut RegisterBlock) }
        }
    }

    pub fn get_time(&self) -> u32 {
        self.p.cvr.read()
    }

    pub fn set_reload(&mut self, reload_value: u32) {
        unsafe { self.p.rvr.write(reload_value) }
    }
}

pub fn example_usage() -> String {
    let mut st = SystemTimer::new();
    st.set_reload(0x00FF_FFFF);
    format!("Time is now 0x{:08x}", st.get_time())
}
```

这种做法的问题是，下面的代码对编译器来说完全可以接受：

```rust,ignore
fn thread1() {
    let mut st = SystemTimer::new();
    st.set_reload(2000);
}

fn thread2() {
    let mut st = SystemTimer::new();
    st.set_reload(1000);
}
```

`set_reload` 函数的 `&mut self` 参数会检查没有其他引用指向*那个特定的* `SystemTimer` 结构体，但它们并不能阻止用户再创建一个指向完全同一外设的第二个 `SystemTimer`！按这种方式编写的代码，若作者足够细心、能发现所有这些「重复」的驱动实例，就能正常工作；但一旦代码分散到多个模块、驱动、开发者和多天的工作中，犯这类错误就会越来越容易。
