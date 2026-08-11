+++
title = "4.7 练习：泛型 `min`"
date = 2026-08-11T11:30:00+08:00
weight = 92
type = "docs"
description = "练习：泛型 `min` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/generics/exercise.html](https://google.github.io/comprehensive-rust/generics/exercise.html)

# 4.7 练习：泛型 `min`

在这个短练习中，你将实现一个泛型 `min` 函数，用 [`Ord`] trait 判断两个值中的较小者。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::cmp::Ordering;

// TODO: 实现测试中用到的 `min` 函数。

#[test]
fn integers() {
    assert_eq!(min(0, 10), 0);
    assert_eq!(min(500, 123), 123);
}

#[test]
fn chars() {
    assert_eq!(min('a', 'z'), 'a');
    assert_eq!(min('7', '1'), '1');
}

#[test]
fn strings() {
    assert_eq!(min("hello", "goodbye"), "goodbye");
    assert_eq!(min("bat", "armadillo"), "armadillo");
}
```

> - 向学员展示 [`Ord`] trait 与 [`Ordering`] 枚举。


[`Ord`]: https://doc.rust-lang.org/stable/std/cmp/trait.Ord.html
[`Ordering`]: https://doc.rust-lang.org/stable/std/cmp/enum.Ordering.html
