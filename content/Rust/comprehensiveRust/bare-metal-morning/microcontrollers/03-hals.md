+++
title = "3.3 HAL Crate"
date = 2026-08-11T11:30:00+08:00
weight = 301
type = "docs"
description = "03-HAL Crate — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/microcontrollers/hals.html](https://google.github.io/comprehensive-rust/bare-metal/microcontrollers/hals.html)

# 3.3 HAL Crate

许多微控制器的
[HAL crate](https://github.com/rust-embedded/awesome-embedded-rust#hal-implementation-crates)
对外各种外设提供封装。它们通常实现
[`embedded-hal`](https://crates.io/crates/embedded-hal) 中的 trait。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#![no_main]
#![no_std]

extern crate panic_halt as _;

use cortex_m_rt::entry;
use embedded_hal::digital::OutputPin;
use nrf52833_hal::gpio::{Level, p0};
use nrf52833_hal::pac::Peripherals;

#[entry]
fn main() -> ! {
    let p = Peripherals::take().unwrap();

    // 为 GPIO 端口 0 创建 HAL 封装。
    let gpio0 = p0::Parts::new(p.P0);

    // 将 GPIO 0 的引脚 21 与 28 配置为推挽输出。
    let mut col1 = gpio0.p0_28.into_push_pull_output(Level::High);
    let mut row1 = gpio0.p0_21.into_push_pull_output(Level::Low);

    // 引脚 28 置低、引脚 21 置高以点亮 LED。
    col1.set_low().unwrap();
    row1.set_high().unwrap();

    loop {}
}
```

> - `set_low` 与 `set_high` 是 `embedded_hal` 的 `OutputPin` trait 上的方法。
> - 许多 Cortex-M 与 RISC-V 设备都有 HAL crate，包括各类 STM32、GD32、nRF、NXP、MSP430、AVR 与 PIC 微控制器。
>
> 用以下命令运行示例：
>
> ```sh
> cargo embed --bin hal
> ```

