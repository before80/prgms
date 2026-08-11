+++
title = "3.1 原始 MMIO"
date = 2026-08-11T11:30:00+08:00
weight = 299
type = "docs"
description = "01-原始 MMIO — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/microcontrollers/mmio.html](https://google.github.io/comprehensive-rust/bare-metal/microcontrollers/mmio.html)

# 3.1 原始 MMIO

多数微控制器通过内存映射 I/O（memory-mapped IO）访问外设。我们试着点亮 micro:bit 上的一颗 LED：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#![no_main]
#![no_std]

extern crate panic_halt as _;

mod interrupts;

use core::mem::size_of;
use cortex_m_rt::entry;

/// GPIO 端口 0 外设地址
const GPIO_P0: usize = 0x5000_0000;

// GPIO 外设偏移
const PIN_CNF: usize = 0x700;
const OUTSET: usize = 0x508;
const OUTCLR: usize = 0x50c;

// PIN_CNF 字段
const DIR_OUTPUT: u32 = 0x1;
const INPUT_DISCONNECT: u32 = 0x1 << 1;
const PULL_DISABLED: u32 = 0x0 << 2;
const DRIVE_S0S1: u32 = 0x0 << 8;
const SENSE_DISABLED: u32 = 0x0 << 16;

#[entry]
fn main() -> ! {
    // 将 GPIO 0 的引脚 21 与 28 配置为推挽输出。
    let pin_cnf_21 = (GPIO_P0 + PIN_CNF + 21 * size_of::<u32>()) as *mut u32;
    let pin_cnf_28 = (GPIO_P0 + PIN_CNF + 28 * size_of::<u32>()) as *mut u32;
    // SAFETY: 指针指向有效的外设控制寄存器，且不存在别名。
    unsafe {
        pin_cnf_21.write_volatile(
            DIR_OUTPUT
                | INPUT_DISCONNECT
                | PULL_DISABLED
                | DRIVE_S0S1
                | SENSE_DISABLED,
        );
        pin_cnf_28.write_volatile(
            DIR_OUTPUT
                | INPUT_DISCONNECT
                | PULL_DISABLED
                | DRIVE_S0S1
                | SENSE_DISABLED,
        );
    }

    // 引脚 28 置低、引脚 21 置高以点亮 LED。
    let gpio0_outset = (GPIO_P0 + OUTSET) as *mut u32;
    let gpio0_outclr = (GPIO_P0 + OUTCLR) as *mut u32;
    // SAFETY: 指针指向有效的外设控制寄存器，且不存在别名。
    unsafe {
        gpio0_outclr.write_volatile(1 << 28);
        gpio0_outset.write_volatile(1 << 21);
    }

    loop {}
}
```

> - GPIO 0 引脚 21 接到 LED 矩阵的第一列，引脚 28 接到第一行。
>
> 用以下命令运行示例：
>
> ```sh
> cargo embed --bin mmio
> ```

