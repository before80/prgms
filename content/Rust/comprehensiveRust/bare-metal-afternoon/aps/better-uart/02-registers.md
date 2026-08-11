+++
title = "1.5.2 多个寄存器"
date = 2026-08-11T11:30:00+08:00
weight = 321
type = "docs"
description = "02-多个寄存器 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/aps/better-uart/registers.html](https://google.github.io/comprehensive-rust/bare-metal/aps/better-uart/registers.html)

# 1.5.2 多个寄存器

我们可以使用一个结构体来表示 UART 寄存器的内存布局。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[repr(C, align(4))]
pub struct Registers {
    dr: u16,
    _reserved0: [u8; 2],
    rsr: ReceiveStatus,
    _reserved1: [u8; 19],
    fr: Flags,
    _reserved2: [u8; 6],
    ilpr: u8,
    _reserved3: [u8; 3],
    ibrd: u16,
    _reserved4: [u8; 2],
    fbrd: u8,
    _reserved5: [u8; 3],
    lcr_h: u8,
    _reserved6: [u8; 3],
    cr: u16,
    _reserved7: [u8; 3],
    ifls: u8,
    _reserved8: [u8; 3],
    imsc: u16,
    _reserved9: [u8; 2],
    ris: u16,
    _reserved10: [u8; 2],
    mis: u16,
    _reserved11: [u8; 2],
    icr: u16,
    _reserved12: [u8; 2],
    dmacr: u8,
    _reserved13: [u8; 3],
}
```

> - [`#[repr(C)]`](https://doc.rust-lang.org/reference/type-layout.html#the-c-representation)
>   告诉编译器按照相同的顺序排列结构体字段
>   规则与 C 相同。这对于我们的结构具有可预测的布局是必要的，如
>   默认的 Rust 表示允许编译器（除其他外）
>   以它认为合适的方式重新排序字段。

