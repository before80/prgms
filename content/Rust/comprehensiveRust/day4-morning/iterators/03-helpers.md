+++
title = "2.3 `Iterator` 辅助方法"
date = 2026-08-11T11:30:00+08:00
weight = 165
type = "docs"
description = "03-`Iterator` 辅助方法 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/iterators/helpers.html](https://google.github.io/comprehensive-rust/iterators/helpers.html)

# 2.3 `Iterator` 辅助方法

除了定义迭代器行为的 `next` 方法外，`Iterator` trait 还提供了 70 多个辅助方法，可用于构建定制化的迭代器。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let result: i32 = (1..=10) // 创建从 1 到 10 的区间
        .filter(|x| x % 2 == 0) // 只保留偶数
        .map(|x| x * x) // 对每个数平方
        .sum(); // 将所有平方结果求和

    println!("The sum of squares of even numbers from 1 to 10 is: {}", result);
}
```

> - `Iterator` trait 实现了许多常见的函数式集合操作（例如 `map`、`filter`、`reduce` 等）。相关文档都可以在这个 trait 里找到。
>
> - 许多辅助方法会接收原始迭代器，并产出行为不同的新迭代器。这些称为「迭代器适配器方法」（iterator adapter methods）。
>
> - 有些方法（如 `sum` 和 `count`）会消费（consume）迭代器，并取出其中的全部元素。
>
> - 这些方法设计为可链式调用，便于拼出完全符合需求的定制迭代器。
>
> ## 更多探索
>
> - Rust 的迭代器极为高效，且高度可优化。即便把许多适配器方法组合成复杂迭代器，生成的代码仍然可以与等效的命令式实现一样高效。

