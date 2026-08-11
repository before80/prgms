+++
title = "2.2.1.3 Mut"
date = 2026-08-11T11:30:00+08:00
weight = 403
type = "docs"
description = "03-Mut — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/mut.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/mut.html)

# 2.2.1.3 Mut

访问式方法的后缀。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
impl<T> Vec<T> {
    fn get(&self, index: usize) -> Option<&T>;
    fn get_mut(&mut self, index: usize) -> Option<&mut T>;
}

impl<T> [T] {
    fn iter(&self) -> impl Iterator<Item = &T>;
    fn iter_mut(&mut self) -> impl Iterator<Item = &mut T>;
}
```

> - 表示该方法提供对可变引用访问的后缀。
>
> - 需要可变地访问你调用该方法的值。
>
> - Rust 无法抽象可变性，因此无法写出一个既能可变又能不可变使用的方法。取而代之，我们写一对函数：不可变版本用较短名字，可变版本加 `_mut` 后缀。

