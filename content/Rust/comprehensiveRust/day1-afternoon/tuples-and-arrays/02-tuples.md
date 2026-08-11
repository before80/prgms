+++
title = "2.2 元组"
date = 2026-08-11T11:30:00+08:00
weight = 41
type = "docs"
description = "02-元组 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/tuples-and-arrays/tuples.html](https://google.github.io/comprehensive-rust/tuples-and-arrays/tuples.html)

# 2.2 元组

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let t: (i8, bool) = (7, true);
    dbg!(t.0);
    dbg!(t.1);
}
```

> - 与数组一样，元组长度固定。
>
> - 元组把不同类型的值组合成一个复合类型。
>
> - 元组字段可通过句点和下标访问，例如 `t.0`、`t.1`。
>
> - 空元组 `()` 称为“单元类型”（unit type），表示没有返回值，类似于其他语言中的 `void`。
>
> - 与数组不同，元组不能用于 `for` 循环。因为 `for` 循环要求所有元素类型相同，而元组未必如此。
>
> - 无法向元组添加或删除元素。元素个数及其类型在编译期固定，运行时不能改变。

