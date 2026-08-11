+++
title = "3.1 借用与函数"
date = 2026-08-11T11:30:00+08:00
weight = 151
type = "docs"
description = "01-借用与函数 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/lifetimes/simple-borrows.html](https://google.github.io/comprehensive-rust/lifetimes/simple-borrows.html)

# 3.1 借用与函数

作为借用检查的一部分，编译器需要推理借用如何流入与流出函数。最简单的情况下，借用持续整个函数调用期间：

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn borrows(x: &i32) {
    dbg!(x);
}

fn main() {
    let mut val = 123;

    // 为函数调用借用 `val`。
    borrows(&val);

    // 借用已结束，我们可以自由地修改。
    val += 5;
}
```

> - 本例中我们为调用 `borrows` 而借用 `val`。这会限制我们修改 `val` 的能力，但一旦函数调用返回，借用就结束了，我们又可以自由修改。

