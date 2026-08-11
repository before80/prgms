+++
title = "4.4.1 `for` 循环"
date = 2026-08-11T11:30:00+08:00
weight = 29
type = "docs"
description = "01-`for` 循环 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/control-flow-basics/loops/for.html](https://google.github.io/comprehensive-rust/control-flow-basics/loops/for.html)

# 4.4.1 `for` 循环

[`for` 循环](https://doc.rust-lang.org/std/keyword.for.html) 会遍历值的范围或集合中的元素：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    for x in 1..5 {
        dbg!(x);
    }

    for elem in [2, 4, 8, 16, 32] {
        dbg!(elem);
    }
}
```

> - 底层上，`for` 循环使用称为“迭代器”（iterator）的概念来处理对不同范围/集合的遍历。迭代器稍后会更详细讨论。
> - 注意第一个 `for` 循环只迭代到 `4`。演示 `1..=5` 语法表示闭区间范围。

