+++
title = "4.2 题解"
date = 2026-08-11T11:30:00+08:00
weight = 310
type = "docs"
description = "02-题解 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/exercises/bare-metal/solutions-morning.html](https://google.github.io/comprehensive-rust/exercises/bare-metal/solutions-morning.html)

# 4.2 题解

## 指南针

（[返回练习](compass.md)）

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#![no_main]
#![no_std]

extern crate panic_halt as _;

use core::fmt::Write;
use cortex_m_rt::entry;
use embedded_hal::digital::InputPin;
use lsm303agr::{
    AccelMode, AccelOutputDataRate, Lsm303agr, MagMode, MagOutputDataRate,
};
use microbit::Board;
use microbit::display::blocking::Display;
use microbit::hal::twim::Twim;
use microbit::hal::uarte::{Baudrate, Parity, Uarte};
use microbit::hal::{Delay, Timer};
use microbit::pac::twim0::frequency::FREQUENCY_A;

const COMPASS_SCALE: i32 = 30000;
const ACCELEROMETER_SCALE: i32 = 700;

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
    writeln!(serial, "Setting up IMU...").unwrap();
    let i2c = Twim::new(board.TWIM0, board.i2c_internal.into(), FREQUENCY_A::K100);
    let mut imu = Lsm303agr::new_with_i2c(i2c);
    imu.init().unwrap();
    imu.set_mag_mode_and_odr(
        &mut delay,
        MagMode::HighResolution,
        MagOutputDataRate::Hz50,
    )
    .unwrap();
    imu.set_accel_mode_and_odr(
        &mut delay,
        AccelMode::Normal,
        AccelOutputDataRate::Hz50,
    )
    .unwrap();
    let mut imu = imu.into_mag_continuous().ok().unwrap();

    // 设置显示与定时器。
    let mut timer = Timer::new(board.TIMER0);
    let mut display = Display::new(board.display_pins);

    let mut mode = Mode::Compass;
    let mut button_pressed = false;

    writeln!(serial, "Ready.").unwrap();

    loop {
        // 读取指南针数据并记录到串口。
        while !(imu.mag_status().unwrap().xyz_new_data()
            && imu.accel_status().unwrap().xyz_new_data())
        {}
        let compass_reading = imu.magnetic_field().unwrap();
        let accelerometer_reading = imu.acceleration().unwrap();
        writeln!(
            serial,
            "{},{},{}\t{},{},{}",
            compass_reading.x_nt(),
            compass_reading.y_nt(),
            compass_reading.z_nt(),
            accelerometer_reading.x_mg(),
            accelerometer_reading.y_mg(),
            accelerometer_reading.z_mg(),
        )
        .unwrap();

        let mut image = [[0; 5]; 5];
        let (x, y) = match mode {
            Mode::Compass => (
                scale(-compass_reading.x_nt(), -COMPASS_SCALE, COMPASS_SCALE, 0, 4)
                    as usize,
                scale(compass_reading.y_nt(), -COMPASS_SCALE, COMPASS_SCALE, 0, 4)
                    as usize,
            ),
            Mode::Accelerometer => (
                scale(
                    accelerometer_reading.x_mg(),
                    -ACCELEROMETER_SCALE,
                    ACCELEROMETER_SCALE,
                    0,
                    4,
                ) as usize,
                scale(
                    -accelerometer_reading.y_mg(),
                    -ACCELEROMETER_SCALE,
                    ACCELEROMETER_SCALE,
                    0,
                    4,
                ) as usize,
            ),
        };
        image[y][x] = 255;
        display.show(&mut timer, image, 100);

        // 若按下按钮 A，切换到下一模式并短暂点亮全部 LED。
        if board.buttons.button_a.is_low().unwrap() {
            if !button_pressed {
                mode = mode.next();
                display.show(&mut timer, [[255; 5]; 5], 200);
            }
            button_pressed = true;
        } else {
            button_pressed = false;
        }
    }
}

#[derive(Copy, Clone, Debug, Eq, PartialEq)]
enum Mode {
    Compass,
    Accelerometer,
}

impl Mode {
    fn next(self) -> Self {
        match self {
            Self::Compass => Self::Accelerometer,
            Self::Accelerometer => Self::Compass,
        }
    }
}

fn scale(value: i32, min_in: i32, max_in: i32, min_out: i32, max_out: i32) -> i32 {
    let range_in = max_in - min_in;
    let range_out = max_out - min_out;
    let scaled = min_out + range_out * (value - min_in) / range_in;
    scaled.clamp(min_out, max_out)
}
```
