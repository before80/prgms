+++
title = "3.4 板级支持 Crate"
date = 2026-08-11T11:30:00+08:00
weight = 302
type = "docs"
description = "04-板级支持 Crate — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/microcontrollers/board-support.html](https://google.github.io/comprehensive-rust/bare-metal/microcontrollers/board-support.html)

# 3.4 板级支持 Crate

板级支持（board support）crate 针对具体开发板再包一层，用起来更方便。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#![no_main]
#![no_std]

extern crate panic_halt as _;

use cortex_m_rt::entry;
use embedded_hal::digital::OutputPin;
use microbit::Board;

#[entry]
fn main() -> ! {
    let mut board = Board::take().unwrap();

    board.display_pins.col1.set_low().unwrap();
    board.display_pins.row1.set_high().unwrap();

    loop {}
}
```

> - 本例中板级支持 crate 主要提供更有用的命名，以及一点初始化。
> - crate 也可能包含微控制器之外某些板载设备的驱动。
>   - `microbit-v2` 包含 LED 矩阵的简单驱动。
>
> 用以下命令运行示例：
>
> ```sh
> cargo embed --bin board_support
> ```

