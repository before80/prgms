+++
title = "8.6 `PhantomPinned` 标记类型"
date = 2026-08-11T11:30:00+08:00
weight = 552
type = "docs"
description = "06-`PhantomPinned` 标记类型 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/phantompinned.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/phantompinned.html)

# 8.6 `PhantomPinned` 标记类型

## 定义

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub struct PhantomPinned;

impl !Unpin for PhantomPinned {}
```

## 用法

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub struct DynamicBuffer {
    data: Vec<u8>,
    cursor: std::ptr::NonNull<u8>,
    _pin: std::marker::PhantomPinned,
}
```

> `PhantomPinned` 是一种标记类型。
>
> 若类型包含 `PhantomPinned`，默认不会实现 `Unpin`。
>
> 当 `DynamicBuffer` 被 `Pin` 包装时，这会产生强制 pinning 的效果。

