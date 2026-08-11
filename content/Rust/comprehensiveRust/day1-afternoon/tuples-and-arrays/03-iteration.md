+++
title = "2.3 数组迭代"
date = 2026-08-11T11:30:00+08:00
weight = 42
type = "docs"
description = "03-数组迭代 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/tuples-and-arrays/iteration.html](https://google.github.io/comprehensive-rust/tuples-and-arrays/iteration.html)

# 2.3 数组迭代

`for` 语句支持遍历数组（但不支持元组）。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let primes = [2, 3, 5, 7, 11, 13, 17, 19];
    for prime in primes {
        for i in 2..prime {
            assert_ne!(prime % i, 0);
        }
    }
}
```

> 该功能依赖 `IntoIterator` trait，但我们尚未讲到。
>
> 这里首次出现 `assert_ne!` 宏。还有 `assert_eq!` 与 `assert!`。这些宏总会检查；而 `debug_assert!` 等仅调试版变体在 release 构建中会编译为空操作。

