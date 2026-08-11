+++
title = "3.2.3 关联类型"
date = 2026-08-11T11:30:00+08:00
weight = 81
type = "docs"
description = "03-关联类型 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/methods-and-traits/traits/associated-types.html](https://google.github.io/comprehensive-rust/methods-and-traits/traits/associated-types.html)

# 3.2.3 关联类型

关联类型（associated types）是由 trait 实现方提供的占位类型。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug)]
struct Meters(i32);
#[derive(Debug)]
struct MetersSquared(i32);

trait Multiply {
    type Output;
    fn multiply(&self, other: &Self) -> Self::Output;
}

impl Multiply for Meters {
    type Output = MetersSquared;
    fn multiply(&self, other: &Self) -> Self::Output {
        MetersSquared(self.0 * other.0)
    }
}

fn main() {
    println!("{:?}", Meters(10).multiply(&Meters(20)));
}
```

> - 关联类型有时也叫「输出类型」。关键点是：由实现方（而非调用方）选择该类型。
>
> - 许多标准库 trait 都有关联类型，包括算术运算符与 `Iterator`。

