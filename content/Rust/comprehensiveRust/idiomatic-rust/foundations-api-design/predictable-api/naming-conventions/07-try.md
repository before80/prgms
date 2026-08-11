+++
title = "2.2.1.7 Try"
date = 2026-08-11T11:30:00+08:00
weight = 407
type = "docs"
description = "07-Try — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/try.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/try.html)

# 2.2.1.7 Try

返回 `Result` 的可失败方法的前缀。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
impl TryFrom<i32> for u32 {
    type Error = TryFromIntError;

    fn try_from(value: i32) -> Result<i64, TryFromIntError>;
}

impl<T> Receiver<T> {
    fn try_recv(&self) -> Result<T, TryRecvError>;
}
```

> - 可能失败并返回 `Result` 的方法前缀。
>
> - `TryFrom` 是类似 `From` 的 trait，用于单值构造可能以某种方式失败的类型。
>
> - 问：为何 `Vec::get` 及其他类似方法不叫 `try_get`？
>
>   若方法返回对已有值的引用，且因只有一种失败模式而返回 `Option` 而非 `Result`，则命名为 `get`。例如，`Vec::get` 只有“索引越界”，`HashMap::get` 只有“键不存在”。

