+++
title = "3.2 返回借用"
date = 2026-08-11T11:30:00+08:00
weight = 152
type = "docs"
description = "02-返回借用 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/lifetimes/returning-borrows.html](https://google.github.io/comprehensive-rust/lifetimes/returning-borrows.html)

# 3.2 返回借用

但函数也可以返回引用！这意味着借用会从函数中流回：

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn identity(x: &i32) -> &i32 {
    x
}

fn main() {
    let mut x = 123;

    let out = identity(&x);

    // x = 5; // 🛠️❌ `x` 仍被借用！

    dbg!(out);
}
```

> - Rust 函数可以返回引用，意味着借用可以从函数中流回。
>
> - 若函数返回引用（或其他形式的借用），它很可能派生自某个参数。这意味着函数的返回值会延长一个或多个参数借用。
>
> - 本例仍然相当简单：只有一个借用传入函数，因此返回的借用必然是同一个。

