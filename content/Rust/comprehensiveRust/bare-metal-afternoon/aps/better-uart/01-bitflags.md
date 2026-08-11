+++
title = "1.5.1 位标志"
date = 2026-08-11T11:30:00+08:00
weight = 320
type = "docs"
description = "01-位标志 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/aps/better-uart/bitflags.html](https://google.github.io/comprehensive-rust/bare-metal/aps/better-uart/bitflags.html)

# 1.5.1 位标志

[`bitflags`](https://crates.io/crates/bitflags) crate 很适合处理位标志。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use bitflags::bitflags;

bitflags! {
    /// 来自 UART 标志寄存器的标志。
    #[repr(transparent)]
    #[derive(Copy, Clone, Debug, Eq, PartialEq)]
    struct Flags: u16 {
        /// 清除发送。
        const CTS = 1 << 0;
        /// 数据集准备就绪。
        const DSR = 1 << 1;
        /// 数据载体检测。
        const DCD = 1 << 2;
        ///UART 忙于传输数据。
        const BUSY = 1 << 3;
        /// 接收 FIFO 为空。
        const RXFE = 1 << 4;
        /// 发送 FIFO 已满。
        const TXFF = 1 << 5;
        /// 接收 FIFO 已满。
        const RXFF = 1 << 6;
        /// 发送 FIFO 为空。
        const TXFE = 1 << 7;
        /// 响铃指示器。
        const RI = 1 << 8;
    }
}
```

> - 这`bitflags!`宏创建一个新类型，类似于`struct Flags(u16)`,
>   以及一堆用于获取和设置标志的方法实现。

