+++
title = "1.7.1 使用它"
date = 2026-08-11T11:30:00+08:00
weight = 327
type = "docs"
description = "01-使用它 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/aps/logging/using.html](https://google.github.io/comprehensive-rust/bare-metal/aps/logging/using.html)

# 1.7.1 使用它

我们需要在使用记录器之前对其进行初始化。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#![no_main]
#![no_std]

mod asm;
mod exceptions;
mod logger;
mod pl011;

use crate::pl011::Uart;
use core::panic::PanicInfo;
use core::ptr::NonNull;
use log::{LevelFilter, error, info};
use safe_mmio::UniqueMmioPointer;
use smccc::Hvc;
use smccc::psci::system_off;

/// 主 PL011 UART 的基地址。
const PL011_BASE_ADDRESS: NonNull<pl011::Registers> =
    NonNull::new(0x900_0000 as _).unwrap();

// 安全：没有此名称的其他全局函数。
#[unsafe(no_mangle)]
extern "C" fn main(x0: u64, x1: u64, x2: u64, x3: u64) {
    // 安全：`PL011_BASE_ADDRESS`是 PL011 设备的基地址，并且
    // 没有其他东西可以访问该地址范围。
    let uart = unsafe { Uart::new(UniqueMmioPointer::new(PL011_BASE_ADDRESS)) };
    logger::init(uart, LevelFilter::Trace).unwrap();

    info!("main({x0:#x}, {x1:#x}, {x2:#x}, {x3:#x})");

    assert_eq!(x1, 42);

    system_off::<Hvc>().unwrap();
}

#[panic_handler]
fn panic(info: &PanicInfo) -> ! {
    error!("{info}");
    system_off::<Hvc>().unwrap();
    loop {}
}
```

> - 请注意，我们的恐慌处理程序现在可以记录恐慌的详细信息。
> - 在 QEMU 中运行示例`make qemu_logger`在下面
>   `src/bare-metal/aps/examples`.

