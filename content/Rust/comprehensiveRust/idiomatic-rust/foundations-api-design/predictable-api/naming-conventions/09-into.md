+++
title = "2.2.1.9 Into"
date = 2026-08-11T11:30:00+08:00
weight = 409
type = "docs"
description = "09-Into — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/into.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/into.html)

# 2.2.1.9 Into

把 `self` 转换为另一类型的方法前缀。消费 `self`，返回拥有所有权的值。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub trait IntoIterator {
    fn into_iter(self) -> Self::IntoIter;
}

impl str {
    fn into_string(self: Box<str>) -> String;
}
```

> - 消费拥有所有权的值并将其变换为另一类型值的函数前缀。
>
> - 不是重新解释转换（reinterpret cast）！数据可被重排、重新分配、以任意方式改变，包括丢失信息。
>
> - `into_iter` 消费一个集合（如 vec、btreeset 或 hashmap）并产生拥有所有权值的迭代器，不同于产生引用值迭代器的 `iter` 与 `iter_mut`。

