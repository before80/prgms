+++
title = "1.6 安全MMIO"
date = 2026-08-11T11:30:00+08:00
weight = 323
type = "docs"
description = "安全MMIO — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/aps/safemmio/registers.html](https://google.github.io/comprehensive-rust/bare-metal/aps/safemmio/registers.html)

# 1.6 安全MMIO

这 [`safe-mmio`] crate 提供了包装寄存器的类型，这些寄存器可以读取或
安全地写。

|             |无法阅读 |阅读无副作用 |阅读有副作用|
| ----------- | ------------- | ------------------------ | -------------------- |
|写不出来|               | [`ReadPure`]             | [`ReadOnly`] |
|可以写| [`WriteOnly`] | [`ReadPureWrite`]        | [`ReadWrite`]         |

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use safe_mmio::fields::{ReadPure, ReadPureWrite, ReadWrite, WriteOnly};

#[repr(C, align(4))]
pub struct Registers {
    dr: ReadWrite<u16>,
    _reserved0: [u8; 2],
    rsr: ReadPure<ReceiveStatus>,
    _reserved1: [u8; 19],
    fr: ReadPure<Flags>,
    _reserved2: [u8; 6],
    ilpr: ReadPureWrite<u8>,
    _reserved3: [u8; 3],
    ibrd: ReadPureWrite<u16>,
    _reserved4: [u8; 2],
    fbrd: ReadPureWrite<u8>,
    _reserved5: [u8; 3],
    lcr_h: ReadPureWrite<u8>,
    _reserved6: [u8; 3],
    cr: ReadPureWrite<u16>,
    _reserved7: [u8; 3],
    ifls: ReadPureWrite<u8>,
    _reserved8: [u8; 3],
    imsc: ReadPureWrite<u16>,
    _reserved9: [u8; 2],
    ris: ReadPure<u16>,
    _reserved10: [u8; 2],
    mis: ReadPure<u16>,
    _reserved11: [u8; 2],
    icr: WriteOnly<u16>,
    _reserved12: [u8; 2],
    dmacr: ReadPureWrite<u8>,
    _reserved13: [u8; 3],
}
```

- 阅读`dr`有一个副作用：它从接收 FIFO 中弹出一个字节。
- 阅读`rsr`（和其他寄存器）没有副作用。这是一本“纯粹”的读物。

> - 有许多不同的 crate 围绕 MMIO 提供安全抽象
>   运营;我们推荐`safe-mmio`箱。
> - 之间的区别`ReadPure` or `ReadOnly`（同样在之间
>   `ReadPureWrite`和`ReadWrite`) 是读寄存器是否可以有
>   改变设备状态的副作用，例如读取数据
>   寄存器从接收 FIFO 中弹出一个字节。`ReadPure`意味着读取有
>   没有副作用，它们纯粹是读取数据。


[`safe-mmio`]: https://crates.io/crates/safe-mmio
[`ReadOnly`]: https://docs.rs/safe-mmio/latest/safe_mmio/fields/struct.ReadOnly.html
[`ReadPure`]: https://docs.rs/safe-mmio/latest/safe_mmio/fields/struct.ReadPure.html
[`ReadPureWrite`]: https://docs.rs/safe-mmio/latest/safe_mmio/fields/struct.ReadPureWrite.html
[`ReadWrite`]: https://docs.rs/safe-mmio/latest/safe_mmio/fields/struct.ReadWrite.html
[`WriteOnly`]: https://docs.rs/safe-mmio/latest/safe_mmio/fields/struct.WriteOnly.html
