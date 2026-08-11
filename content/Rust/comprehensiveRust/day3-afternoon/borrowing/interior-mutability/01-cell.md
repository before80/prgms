+++
title = "2.4.1 `Cell`"
date = 2026-08-11T11:30:00+08:00
weight = 146
type = "docs"
description = "01-`Cell` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/borrowing/interior-mutability/cell.html](https://google.github.io/comprehensive-rust/borrowing/interior-mutability/cell.html)

# 2.4.1 `Cell`

`Cell` 包装一个值，并允许仅通过指向 `Cell` 的共享引用来获取或设置该值。但它不允许任何指向内部值的引用。由于没有引用，借用规则也就无法被破坏。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::cell::Cell;

fn main() {
    // 注意：`cell` 并未声明为可变。
    let cell = Cell::new(5);

    cell.set(123);
    dbg!(cell.get());
}
```

> - `Cell` 是一种简单的安全保障手段：它有一个接受 `&self` 的 `set` 方法。这不需要运行时检查，但要求移动值，而这本身也可能有成本。

