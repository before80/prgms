+++
title = "3.5 类型状态模式"
date = 2026-08-11T11:30:00+08:00
weight = 303
type = "docs"
description = "05-类型状态模式 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/microcontrollers/type-state.html](https://google.github.io/comprehensive-rust/bare-metal/microcontrollers/type-state.html)

# 3.5 类型状态模式

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[entry]
fn main() -> ! {
    let p = Peripherals::take().unwrap();
    let gpio0 = p0::Parts::new(p.P0);

    let pin: P0_01<Disconnected> = gpio0.p0_01;

    // let gpio0_01_again = gpio0.p0_01; // 错误，已移动。
    let mut pin_input: P0_01<Input<Floating>> = pin.into_floating_input();
    if pin_input.is_high().unwrap() {
        // ...
    }
    let mut pin_output: P0_01<Output<OpenDrain>> = pin_input
        .into_open_drain_output(OpenDrainConfig::Disconnect0Standard1, Level::Low);
    pin_output.set_high().unwrap();
    // pin_input.is_high(); // 错误，已移动。

    let _pin2: P0_02<Output<OpenDrain>> = gpio0
        .p0_02
        .into_open_drain_output(OpenDrainConfig::Disconnect0Standard1, Level::Low);
    let _pin3: P0_03<Output<PushPull>> =
        gpio0.p0_03.into_push_pull_output(Level::Low);

    loop {}
}
```

> - 引脚不实现 `Copy` 或 `Clone`，因此每个引脚只能有一个实例。一旦引脚从端口结构体中移出，别人就无法再取走它。
> - 更改引脚配置会消费旧的引脚实例，因此之后不能再使用旧实例。
> - 值的类型表明它所处的状态：例如本例中是 GPIO 引脚的配置状态。这把状态机编码进类型系统，确保你不会在未正确配置的情况下以某种方式使用引脚。非法状态转换会在编译期被捕获。
> - 你可以在输入引脚上调用 `is_high`，在输出引脚上调用 `set_high`，反之不行。
> - 许多 HAL crate 遵循这一模式。

