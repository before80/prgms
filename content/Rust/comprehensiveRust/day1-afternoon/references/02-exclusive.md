+++
title = "3.2 独占引用"
date = 2026-08-11T11:30:00+08:00
weight = 48
type = "docs"
description = "02-独占引用 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/references/exclusive.html](https://google.github.io/comprehensive-rust/references/exclusive.html)

# 3.2 独占引用

独占引用（也称为可变引用）允许修改它们所指向的值。类型为 `&mut T`。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let mut point = (1, 2);
    let x_coord = &mut point.0;
    *x_coord = 20;
    println!("point: {point:?}");
}
```

> 要点：
>
> - “独占”意味着只能通过这个引用访问该值。同时不能存在其他引用（共享或独占），且在独占引用存活期间也不能直接访问被引用的值。试试在 `x_coord` 仍存活时创建 `&point.0` 或修改 `point.0`。
>
> - 务必区分 `let mut x_coord: &i32` 与 `let x_coord: &mut i32`。前者是可以重新绑定到不同值的共享引用，后者是指向可变值的独占引用。

