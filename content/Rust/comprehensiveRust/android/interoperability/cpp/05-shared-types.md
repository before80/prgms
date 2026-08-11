+++
title = "7.2.5 共享类型"
date = 2026-08-11T11:30:00+08:00
weight = 246
type = "docs"
description = "05-共享类型 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability/cpp/shared-types.html](https://google.github.io/comprehensive-rust/android/interoperability/cpp/shared-types.html)

# 7.2.5 共享类型

```rust,ignore
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[cxx::bridge]
mod ffi {
    #[derive(Clone, Debug, Hash)]
    struct PlayingCard {
        suit: Suit,
        value: u8,  // A=1, J=11, Q=12, K=13
    }

    enum Suit {
        Clubs,
        Diamonds,
        Hearts,
        Spades,
    }
}
```

> - 只支持类 C（unit）枚举。
> - 共享类型上的 `#[derive()]` 只支持有限数量的 trait。对应功能也会为 C++ 代码生成，例如若你 derive `Hash`，也会为对应的 C++ 类型生成 `std::hash` 实现。

