+++
title = "3 微控制器"
date = 2026-08-11T11:30:00+08:00
weight = 298
type = "docs"
description = "微控制器 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/microcontrollers.html](https://google.github.io/comprehensive-rust/bare-metal/microcontrollers.html)

# 3 微控制器

`cortex_m_rt` crate（除其他功能外）为 Cortex M 微控制器提供复位处理程序（reset handler）。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#![no_main]
#![no_std]

extern crate panic_halt as _;

mod interrupts;

use cortex_m_rt::entry;

#[entry]
fn main() -> ! {
    loop {}
}
```

接下来我们会看如何访问外设，抽象层级逐步提高。

> - `cortex_m_rt::entry` 宏要求函数类型为 `fn() -> !`，因为返回到复位处理程序没有意义。
> - 用 `cargo embed --bin minimal` 运行示例。

