+++
title = "3.2 PAC"
date = 2026-08-11T11:30:00+08:00
weight = 300
type = "docs"
description = "02-PAC — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/microcontrollers/pacs.html](https://google.github.io/comprehensive-rust/bare-metal/microcontrollers/pacs.html)

# 3.2 PAC

[`svd2rust`](https://crates.io/crates/svd2rust) 根据
[CMSIS-SVD](https://www.keil.com/pack/doc/CMSIS/SVD/html/index.html) 文件，为内存映射外设生成大多安全的 Rust 封装。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#![no_main]
#![no_std]

extern crate panic_halt as _;

use cortex_m_rt::entry;
use nrf52833_pac::Peripherals;

#[entry]
fn main() -> ! {
    let p = Peripherals::take().unwrap();
    let gpio0 = p.P0;

    // 将 GPIO 0 的引脚 21 与 28 配置为推挽输出。
    gpio0.pin_cnf[21].write(|w| {
        w.dir().output();
        w.input().disconnect();
        w.pull().disabled();
        w.drive().s0s1();
        w.sense().disabled();
        w
    });
    gpio0.pin_cnf[28].write(|w| {
        w.dir().output();
        w.input().disconnect();
        w.pull().disabled();
        w.drive().s0s1();
        w.sense().disabled();
        w
    });

    // 引脚 28 置低、引脚 21 置高以点亮 LED。
    gpio0.outclr.write(|w| w.pin28().clear());
    gpio0.outset.write(|w| w.pin21().set());

    loop {}
}
```

> - SVD（System View Description）文件是芯片厂商通常提供的 XML，描述设备的内存映射。
>   - 按外设、寄存器、字段与取值组织，包含名称、描述、地址等。
>   - SVD 文件常常有缺陷或不完整，因此有各种项目会修补错误、补全缺失细节，并发布生成的 crate。
> - `cortex-m-rt` 提供向量表等基础设施。
> - 若已 `cargo install cargo-binutils`，可运行
>   `cargo objdump --bin pac -- -d --no-show-raw-insn` 查看生成的二进制。
>
> 用以下命令运行示例：
>
> ```sh
> cargo embed --bin pac
> ```

