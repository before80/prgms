+++
title = "06-异常"
date = 2026-08-01T10:38:00+08:00
weight = 44
type = "docs"
description = "异常（Exceptions）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 异常 {#exceptions}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/start/exceptions.html](https://doc.rust-lang.org/stable/embedded-book/start/exceptions.html)


异常（exception）与中断是处理器处理异步事件与致命错误（例如执行无效指令）的硬件机制。异常意味着抢占，并涉及异常处理函数——响应触发该事件的信号而执行的子例程。

`cortex-m-rt` crate 提供 [`exception`] 属性来声明异常处理函数。

[`exception`]: https://docs.rs/cortex-m-rt-macros/latest/cortex_m_rt_macros/attr.exception.html

``` rust,ignore
// SysTick（系统定时器）异常的异常处理函数
#[exception]
fn SysTick() {
    // ..
}
```

除了 `exception` 属性外，异常处理函数看起来像普通函数，但还有一个区别：`exception` 处理函数*不能*被软件调用。沿用上例，语句 `SysTick();` 会导致编译错误。

这种行为基本上是有意为之，并且是为了提供一项特性：在 `exception` 处理函数*内部*声明的 `static mut` 变量可以*安全*使用。

``` rust,ignore
#[exception]
fn SysTick() {
    static mut COUNT: u32 = 0;

    // `COUNT` 已变为 `&mut u32` 类型，可以安全使用
    *COUNT += 1;
}
```

如你所知，在函数中使用 `static mut` 变量会使它成为[*不可重入*](https://en.wikipedia.org/wiki/Reentrancy_(computing))的。从多个异常/中断处理函数，或从 `main` 与一个或多个异常/中断处理函数，直接或间接调用不可重入函数，是未定义行为。

Safe Rust 绝不能导致未定义行为，因此不可重入函数必须标为 `unsafe`。但我刚才说 `exception` 处理函数可以安全使用 `static mut` 变量。这怎么可能？这之所以可能，是因为 `exception` 处理函数*不能*被软件调用，因此不存在重入。这些处理函数由硬件本身调用，并假定硬件在物理上是非并发的。

因此，在嵌入式系统的异常处理函数语境中，同一处理函数不存在并发调用，确保即使处理函数使用静态可变变量，也不会有重入问题。

在多核系统中，多个处理器内核并发执行代码，即使在异常处理函数内部，重入问题的可能性也会再次变得相关。虽然每个内核可能有自己的一组异常处理函数，但仍然可能出现多个内核同时试图执行同一异常处理函数的场景。
为在多核环境中解决这一顾虑，需要在异常处理函数内采用适当的同步机制，以确保对各内核间共享资源的访问得到妥善协调。这通常涉及锁、信号量或原子操作等技术，以防止数据竞争并维护数据完整性。

> 注意：`exception` 属性会变换函数内部静态变量的定义，把它们包进 `unsafe` 块，并为我们提供同名的、类型为 `&mut` 的新的合适变量。
> 因此我们可以通过 `*` 解引用该引用以访问变量的值，而无需把它们包在 `unsafe` 块中。

## 完整示例 {#a-complete-example}

下面是一个使用系统定时器大约每秒触发一次 `SysTick` 异常的例子。`SysTick` 异常处理函数在 `COUNT` 变量中跟踪自己被调用的次数，然后用半主机把 `COUNT` 的值打印到主机控制台。

> **注意**：你可以在任何 Cortex-M 设备上运行此示例；也可以在 QEMU 上运行。

```rust,ignore
#![deny(unsafe_code)]
#![no_main]
#![no_std]

use panic_halt as _;

use core::fmt::Write;

use cortex_m::peripheral::syst::SystClkSource;
use cortex_m_rt::{entry, exception};
use cortex_m_semihosting::{
    debug,
    hio::{self, HostStream},
};

#[entry]
fn main() -> ! {
    let p = cortex_m::Peripherals::take().unwrap();
    let mut syst = p.SYST;

    // 配置系统定时器每秒触发一次 SysTick 异常
    syst.set_clock_source(SystClkSource::Core);
    // 这是为默认 CPU 时钟为 12 MHz 的 LM3S6965 配置的
    syst.set_reload(12_000_000);
    syst.clear_current();
    syst.enable_counter();
    syst.enable_interrupt();

    loop {}
}

#[exception]
fn SysTick() {
    static mut COUNT: u32 = 0;
    static mut STDOUT: Option<HostStream> = None;

    *COUNT += 1;

    // 惰性初始化
    if STDOUT.is_none() {
        *STDOUT = hio::hstdout().ok();
    }

    if let Some(hstdout) = STDOUT.as_mut() {
        write!(hstdout, "{}", *COUNT).ok();
    }

    // 重要：若在真实硬件上运行，请省略此 `if` 块，否则你的
    // 调试器会进入不一致状态
    if *COUNT == 9 {
        // 这将终止 QEMU 进程
        debug::exit(debug::EXIT_SUCCESS);
    }
}
```

``` console
tail -n5 Cargo.toml
```

``` toml
[dependencies]
cortex-m = "0.5.7"
cortex-m-rt = "0.6.3"
panic-halt = "0.2.0"
cortex-m-semihosting = "0.3.1"
```

``` text
$ cargo run --release
     Running `qemu-system-arm -cpu cortex-m3 -machine lm3s6965evb (..)
123456789
```

若你在 Discovery 开发板上运行，会在 OpenOCD 控制台看到输出。此外，当计数到达 9 时程序*不会*停止。

## 默认异常处理函数 {#the-default-exception-handler}

`exception` 属性实际做的是*覆盖*特定异常的默认异常处理函数。若你没有覆盖某个特定异常的处理函数，它将由 `DefaultHandler` 函数处理，其默认实现为：

``` rust,ignore
fn DefaultHandler() {
    loop {}
}
```

该函数由 `cortex-m-rt` crate 提供，并标为 `#[no_mangle]`，因此你可以在 “DefaultHandler” 上设断点并捕获*未处理*的异常。

可以用 `exception` 属性覆盖这个 `DefaultHandler`：

``` rust,ignore
#[exception]
fn DefaultHandler(irqn: i16) {
    // 自定义默认处理函数
}
```

`irqn` 参数表明正在服务哪个异常。负值表示正在服务 Cortex-M 异常；零或正值表示正在服务设备特定异常，即中断。

## HardFault 处理函数 {#the-hard-fault-handler}

`HardFault` 异常有些特殊。当程序进入无效状态时会触发该异常，因此其处理函数*不能*返回，否则可能导致未定义行为。此外，运行时 crate 在调用用户定义的 `HardFault` 处理函数之前会做一些工作，以改善可调试性。

结果是 `HardFault` 处理函数必须具有以下签名：`fn(&ExceptionFrame) -> !`。处理函数的参数是指向异常压入栈中的寄存器的指针。这些寄存器是异常触发瞬间处理器状态的快照，对诊断 hard fault 很有用。

下面是一个执行非法操作的例子：读取不存在的内存位置。

> **注意**：该程序在 QEMU 上不会按预期工作，即它不会崩溃，因为 `qemu-system-arm -machine lm3s6965evb` 不检查内存加载，并会在读取无效内存时愉快地返回 `0`。

```rust,ignore
#![no_main]
#![no_std]

use panic_halt as _;

use core::fmt::Write;
use core::ptr;

use cortex_m_rt::{entry, exception, ExceptionFrame};
use cortex_m_semihosting::hio;

#[entry]
fn main() -> ! {
    // 读取不存在的内存位置
    unsafe {
        ptr::read_volatile(0x3FFF_0000 as *const u32);
    }

    loop {}
}

#[exception]
fn HardFault(ef: &ExceptionFrame) -> ! {
    if let Ok(mut hstdout) = hio::hstdout() {
        writeln!(hstdout, "{:#?}", ef).ok();
    }

    loop {}
}
```

`HardFault` 处理函数打印 `ExceptionFrame` 的值。若你运行它，会在 OpenOCD 控制台看到类似如下内容。

``` text
$ openocd
(..)
ExceptionFrame {
    r0: 0x3fff0000,
    r1: 0x00000003,
    r2: 0x080032e8,
    r3: 0x00000000,
    r12: 0x00000000,
    lr: 0x080016df,
    pc: 0x080016e2,
    xpsr: 0x61000000,
}
```

`pc` 值是异常发生时程序计数器的值，它指向触发异常的指令。

若你查看程序的反汇编：


``` text
$ cargo objdump --bin app --release -- -d --no-show-raw-insn --print-imm-hex
(..)
ResetTrampoline:
 8000942:       movw    r0, #0xfffe
 8000946:       movt    r0, #0x3fff
 800094a:       ldr     r0, [r0]
 800094c:       b       #-0x4 <ResetTrampoline+0xa>
```

你可以在反汇编中查找程序计数器值 `0x0800094a`。你会看到一次加载操作（`ldr r0, [r0]`）导致了异常。`ExceptionFrame` 的 `r0` 字段会告诉你当时寄存器 `r0` 的值是 `0x3fff_fffe`。
