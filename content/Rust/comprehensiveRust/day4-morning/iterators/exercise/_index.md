+++
title = "2.6 练习：迭代器方法链式调用"
date = 2026-08-11T11:30:00+08:00
weight = 168
type = "docs"
description = "练习：迭代器方法链式调用 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/iterators/exercise.html](https://google.github.io/comprehensive-rust/iterators/exercise.html)

# 2.6 练习：迭代器方法链式调用

在本练习中，你需要在 [`Iterator`][1] trait 提供的方法中查找并使用合适的方法，来实现一个稍复杂的计算。

把下面的代码复制到 <https://play.rust-lang.org/>，并让测试通过。请用迭代器表达式，再用 `collect` 收集结果来构造返回值。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 计算 `values` 中各元素与偏移 `offset` 处元素的差，
/// 从末尾绕回到开头（环形）。
///
/// 结果的第 `n` 个元素为 `values[(n+offset)%len] - values[n]`。
fn offset_differences(offset: usize, values: Vec<i32>) -> Vec<i32> {
    todo!()
}

#[test]
fn test_offset_one() {
    assert_eq!(offset_differences(1, vec![1, 3, 5, 7]), vec![2, 2, 2, -6]);
    assert_eq!(offset_differences(1, vec![1, 3, 5]), vec![2, 2, -4]);
    assert_eq!(offset_differences(1, vec![1, 3]), vec![2, -2]);
}

#[test]
fn test_larger_offsets() {
    assert_eq!(offset_differences(2, vec![1, 3, 5, 7]), vec![4, 4, -4, -4]);
    assert_eq!(offset_differences(3, vec![1, 3, 5, 7]), vec![6, -2, -2, -2]);
    assert_eq!(offset_differences(4, vec![1, 3, 5, 7]), vec![0, 0, 0, 0]);
    assert_eq!(offset_differences(5, vec![1, 3, 5, 7]), vec![2, 2, 2, -6]);
}

#[test]
fn test_degenerate_cases() {
    assert_eq!(offset_differences(1, vec![0]), vec![0]);
    assert_eq!(offset_differences(1, vec![1]), vec![0]);
    let empty: Vec<i32> = vec![];
    assert_eq!(offset_differences(1, empty), vec![]);
}
```

[1]: https://doc.rust-lang.org/std/iter/trait.Iterator.html
