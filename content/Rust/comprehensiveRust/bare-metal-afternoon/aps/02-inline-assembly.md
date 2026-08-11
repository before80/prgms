+++
title = "1.2 内联装配"
date = 2026-08-11T11:30:00+08:00
weight = 314
type = "docs"
description = "02-内联装配 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/aps/inline-assembly.html](https://google.github.io/comprehensive-rust/bare-metal/aps/inline-assembly.html)

# 1.2 内联装配

有时我们需要使用汇编来完成 Rust 无法完成的事情
代码。例如，进行 HVC（管理程序调用）来告诉固件
关闭系统电源：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#![no_main]
#![no_std]

use core::arch::asm;
use core::panic::PanicInfo;

mod asm;
mod exceptions;

const PSCI_SYSTEM_OFF: u32 = 0x84000008;

// 安全：没有此名称的其他全局函数。
#[unsafe(no_mangle)]
extern "C" fn main(_x0: u64, _x1: u64, _x2: u64, _x3: u64) {
    // 安全：这仅使用声明的寄存器并且不执行任何操作
    // 有记忆。
    unsafe {
        asm!("hvc #0",
            inout("w0") PSCI_SYSTEM_OFF => _,
            inout("w1") 0 => _,
            inout("w2") 0 => _,
            inout("w3") 0 => _,
            inout("w4") 0 => _,
            inout("w5") 0 => _,
            inout("w6") 0 => _,
            inout("w7") 0 => _,
            options(nomem, nostack)
        );
    }

    loop {}
}
```

（如果您确实想这样做，请使用 [`smccc`][1] 有包装纸的板条箱
对于所有这些功能。）

> - PSCI 是 Arm 电源状态协调接口，是一组标准的
>   管理系统和 CPU 电源状态等功能。它是
>   由许多系统上的 EL3 固件和虚拟机管理程序实现。
> - 这`0 => _`语法意味着在运行之前将寄存器初始化为0
>   内联汇编代码，然后忽略其内容。我们需要使用`inout`而不是`in`因为该调用可能会破坏
>   寄存器的内容。
> - 这`main`函数需要是`#[unsafe(no_mangle)]`和`extern "C"`
>   因为它是从我们的入口点调用的`entry.S`.
>   - 只是`#[no_mangle]`就足够了，但是
>     [RFC3325](https://rust-lang.github.io/rfcs/3325-unsafe-attributes.html) 使用
>     此符号是为了引起审阅者注意可能导致
>     如果使用不正确，则会出现未定义的行为。
> - `_x0`–`_x3`是寄存器的值`x0`–`x3`，这通常是
>   引导加载程序使用它来传递诸如指向设备树的指针之类的东西。
>   根据标准 aarch64 调用约定（这就是`extern "C"`指定使用），寄存器`x0`–`x7`用于前 8 个
>   参数传递给函数，所以`entry.S`不需要做任何事
>   特殊之处在于确保它不会更改这些寄存器。
> - 在 QEMU 中运行示例`make qemu_psci`在下面
>   `src/bare-metal/aps/examples`.


[1]: https://crates.io/crates/smccc
