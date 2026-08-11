+++
title = "2.4 `小维克`"
date = 2026-08-11T11:30:00+08:00
weight = 336
type = "docs"
description = "04-`小维克` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/useful-crates/tinyvec.html](https://google.github.io/comprehensive-rust/bare-metal/useful-crates/tinyvec.html)

# 2.4 `小维克`

有时你想要一些可以像“Vec”一样调整大小的东西，但没有堆
分配。 [`tinyvec`][1] 提供了这个：由数组或切片支持的向量，
它可以静态分配或在堆栈上，跟踪如何
使用了许多元素，如果您尝试使用超过分配的元素，则会出现恐慌。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use tinyvec::{ArrayVec, array_vec};

fn main() {
    let mut numbers: ArrayVec<[u32; 5]> = array_vec!(42, 66);
    println!("{numbers:?}");
    numbers.push(7);
    println!("{numbers:?}");
    numbers.remove(1);
    println!("{numbers:?}");
}
```

> - `tinyvec` 要求元素类型实现 `Default`
>   初始化。
> - Rust Playground 包含 `tinyvec`，因此这个示例可以很好地内联运行。


[1]: https://crates.io/crates/tinyvec
