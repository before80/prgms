+++
title = "2.2.1.1 New"
date = 2026-08-11T11:30:00+08:00
weight = 401
type = "docs"
description = "01-New — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/new.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/new.html)

# 2.2.1.1 New

Rust 没有 `new` 关键字，`new` 反而是常见的前缀或整个方法名。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
impl<T> Vec<T> {
    fn new() -> Vec<T>;
}

impl<T> Box<T> {
    fn new(T) -> Box<T>;
}
```

> - Rust 没有用于初始化新值的 `new` 关键字，只有你调用的函数或直接填充的值。
>
>   `new` 按约定是类型的“默认”构造函数。它没有特殊语法含义。
>
>   它有时是前缀，有时接受参数。

