+++
title = "1.9 aarch64-rt"
date = 2026-08-11T11:30:00+08:00
weight = 329
type = "docs"
description = "aarch64-rt — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/aps/aarch64-rt.html](https://google.github.io/comprehensive-rust/bare-metal/aps/aarch64-rt.html)

# 1.9 aarch64-rt

这`aarch64-rt`crate 提供程序集入口点和异常向量
我们之前实施过。我们只需要用以下标记我们的主要功能`entry!`宏。

它还提供了`initial_pagetable!`宏让我们定义一个初始值
Rust 中的静态页表，而不是像我们之前那样在汇编代码中。

我们还可以使用 UART 驱动程序`arm-pl011-uart`板条箱而不是
写我们自己的。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
#![no_main]
#![no_std]

mod exceptions_rt;

use aarch64_paging::descriptor::El1Attributes;
use aarch64_rt::{InitialPagetable, entry, initial_pagetable};
use arm_pl011_uart::{PL011Registers, Uart, UniqueMmioPointer};
use core::fmt::Write;
use core::panic::PanicInfo;
use core::ptr::NonNull;
use smccc::Hvc;
use smccc::psci::system_off;

/// 主 PL011 UART 的基地址。
const PL011_BASE_ADDRESS: NonNull<PL011Registers> =
    NonNull::new(0x900_0000 as _).unwrap();

/// 用于初始标识映射中的设备内存的属性。
const DEVICE_ATTRIBUTES: El1Attributes = El1Attributes::VALID
    .union(El1Attributes::ATTRIBUTE_INDEX_0)
    .union(El1Attributes::ACCESSED)
    .union(El1Attributes::UXN);

/// 用于初始标识映射中的普通内存的属性。
const MEMORY_ATTRIBUTES: El1Attributes = El1Attributes::VALID
    .union(El1Attributes::ATTRIBUTE_INDEX_1)
    .union(El1Attributes::INNER_SHAREABLE)
    .union(El1Attributes::ACCESSED)
    .union(El1Attributes::NON_GLOBAL);

initial_pagetable!({
    let mut idmap = [0; 512];
    // 1 GiB 设备内存。
    idmap[0] = DEVICE_ATTRIBUTES.bits();
    // 1 GiB 普通内存。
    idmap[1] = MEMORY_ATTRIBUTES.bits() | 0x40000000;
    // 另外 1 GiB 设备内存从 256 GiB 开始。
    idmap[256] = DEVICE_ATTRIBUTES.bits() | 0x4000000000;
    InitialPagetable(idmap)
});

entry!(main);
fn main(x0: u64, x1: u64, x2: u64, x3: u64) -> ! {
    // 安全：`PL011_BASE_ADDRESS`是 PL011 设备的基地址，并且
    // 没有其他东西可以访问该地址范围。
    let mut uart = unsafe { Uart::new(UniqueMmioPointer::new(PL011_BASE_ADDRESS)) };

    writeln!(uart, "main({x0:#x}, {x1:#x}, {x2:#x}, {x3:#x})").unwrap();

    system_off::<Hvc>().unwrap();
    panic!("system_off returned");
}

#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    system_off::<Hvc>().unwrap();
    loop {}
}
```

> - 在 QEMU 中运行示例`make qemu_rt`在下面
>   `src/bare-metal/aps/examples`.

