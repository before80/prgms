+++
title = "4.6 函数"
date = 2026-08-11T11:30:00+08:00
weight = 33
type = "docs"
description = "04-函数 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/control-flow-basics/functions.html](https://google.github.io/comprehensive-rust/control-flow-basics/functions.html)

# 4.6 函数

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn gcd(a: u32, b: u32) -> u32 {
    if b > 0 { gcd(b, a % b) } else { a }
}

fn main() {
    dbg!(gcd(143, 52));
}
```

> - 声明参数后跟类型（与某些编程语言相反），然后是返回类型。
> - 函数体（或任意块）中的最后一个表达式会成为返回值。只需省略表达式末尾的 `;`。`return` 关键字可用于提前返回，但在函数末尾使用“裸值”形式是惯用写法（可把 `gcd` 改写成使用 `return`）。
> - 有些函数没有返回值，返回的是“单元类型”`()`。若省略返回类型，编译器会推断为该类型。
> - 不支持重载——每个函数只有一种实现。
>   - 始终接受固定数量的参数。不支持默认参数。可用宏来支持可变参数函数。
>   - 始终接受一组固定的参数类型。这些类型可以是泛型，稍后会介绍。

