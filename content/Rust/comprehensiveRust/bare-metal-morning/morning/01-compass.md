+++
title = "4.1 指南针"
date = 2026-08-11T11:30:00+08:00
weight = 309
type = "docs"
description = "01-指南针 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/exercises/bare-metal/compass.html](https://google.github.io/comprehensive-rust/exercises/bare-metal/compass.html)

# 4.1 指南针

我们将从 I2C 指南针读取方向，并把读数记录到串口。若有时间，也可以试着在 LED 上显示，或以某种方式使用按钮。

提示：

- 查阅 [`lsm303agr`](https://docs.rs/lsm303agr/latest/lsm303agr/) 与
  [`microbit-v2`](https://docs.rs/microbit-v2/latest/microbit/) crate 的文档，以及
  [micro:bit 硬件说明](https://tech.microbit.org/hardware/)。
- LSM303AGR 惯性测量单元（IMU）接在内部 I2C 总线上。
- TWI 是 I2C 的另一名称，因此 I2C 主机外设叫作 TWIM。
- LSM303AGR 驱动需要实现 `embedded_hal::i2c::I2c` trait 的东西。
  [`microbit::hal::Twim`](https://docs.rs/microbit-v2/latest/microbit/hal/struct.Twim.html)
  结构体实现了该 trait。
- 你有一个
  [`microbit::Board`](https://docs.rs/microbit-v2/latest/microbit/struct.Board.html)
  结构体，包含各类引脚与外设字段。
- 若愿意也可查看
  [nRF52833 数据手册](https://infocenter.nordicsemi.com/pdf/nRF52833_PS_v1.5.pdf)，但完成本练习并非必需。

下载[练习模板](../../comprehensive-rust-exercises.zip)，在 `compass` 目录中查看下列文件。

_src/main.rs_：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#![no_main]
#![no_std]

extern crate panic_halt as _;

use core::fmt::Write;
use cortex_m_rt::entry;
use microbit::{hal::{Delay, uarte::{Baudrate, Parity, Uarte}}, Board};

#[entry]
fn main() -> ! {
    let mut board = Board::take().unwrap();

    // 配置串口。
    let mut serial = Uarte::new(
        board.UARTE0,
        board.uart.into(),
        Parity::EXCLUDED,
        Baudrate::BAUD115200,
    );

    // 用系统定时器作为延时提供者。
    let mut delay = Delay::new(board.SYST);

    // 设置 I2C 控制器与惯性测量单元。
    // TODO

    writeln!(serial, "Ready.").unwrap();

    loop {
        // 读取指南针数据并记录到串口。
        // TODO
    }
}
```

_Cargo.toml_（通常无需修改）：

```toml
[workspace]

[package]
name = "compass"
version = "0.1.0"
edition = "2024"
publish = false

[dependencies]
cortex-m-rt = "0.7.5"
embedded-hal = "1.0.0"
lsm303agr = "1.1.0"
microbit-v2 = "0.16.0"
panic-halt = "1.0.0"
```

_Embed.toml_（通常无需修改）：

```toml
[default.general]
chip = "nrf52833_xxAA"

[debug.gdb]
enabled = true

[debug.reset]
halt_afterwards = true
```

_.cargo/config.toml_（通常无需修改）：

```toml
[build]
target = "thumbv7em-none-eabihf" # Cortex-M4F

[target.'cfg(all(target_arch = "arm", target_os = "none"))']
rustflags = ["-C", "link-arg=-Tlink.x"]
```

在 Linux 上查看串口输出：

```sh
picocom --baud 115200 --imap lfcrlf /dev/ttyACM0
```

在 Mac OS 上大致如下（设备名可能略有不同）：

```sh
picocom --baud 115200 --imap lfcrlf /dev/tty.usbmodem14502
```

用 Ctrl+A Ctrl+Q 退出 picocom。
