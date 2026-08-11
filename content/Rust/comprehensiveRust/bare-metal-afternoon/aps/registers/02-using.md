+++
title = "1.6.2 使用它"
date = 2026-08-11T11:30:00+08:00
weight = 325
type = "docs"
description = "02-使用它 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/aps/safemmio/using.html](https://google.github.io/comprehensive-rust/bare-metal/aps/safemmio/using.html)

# 1.6.2 使用它

让我们使用我们的驱动程序编写一个小程序来写入串行控制台，然后
回显传入的字节。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
#![no_main]
#![no_std]

mod asm;
mod exceptions;
mod pl011;

use crate::pl011::Uart;
use core::fmt::Write;
use core::panic::PanicInfo;
use core::ptr::NonNull;
use log::error;
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
    let mut uart = Uart::new(unsafe { UniqueMmioPointer::new(PL011_BASE_ADDRESS) });

    writeln!(uart, "main({x0:#x}, {x1:#x}, {x2:#x}, {x3:#x})").unwrap();

    loop {
        if let Some(byte) = uart.read_byte() {
            uart.write_byte(byte);
            match byte {
                b'\r' => uart.write_byte(b'\n'),
                b'q' => break,
                _ => continue,
            }
        }
    }

    writeln!(uart, "\n\nBye!").unwrap();
    system_off::<Hvc>().unwrap();
}
```

> - 在 QEMU 中运行示例`make qemu_safemmio`在下面
>   `src/bare-metal/aps/examples`.

