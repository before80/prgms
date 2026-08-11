+++
title = "3.6.1 解答"
date = 2026-08-11T11:30:00+08:00
weight = 53
type = "docs"
description = "01-解答 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/references/solution.html](https://google.github.io/comprehensive-rust/references/solution.html)

# 3.6.1 解答

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 计算给定向量的模长。
fn magnitude(vector: &[f64; 3]) -> f64 {
    let mut mag_squared = 0.0;
    for coord in vector {
        mag_squared += coord * coord;
    }
    mag_squared.sqrt()
}

/// 在不改变方向的前提下，把向量的模长变为 1.0。
fn normalize(vector: &mut [f64; 3]) {
    let mag = magnitude(vector);
    for item in vector {
        *item /= mag;
    }
}

fn main() {
    println!("Magnitude of a unit vector: {}", magnitude(&[0.0, 1.0, 0.0]));

    let mut v = [1.0, 2.0, 9.0];
    println!("Magnitude of {v:?}: {}", magnitude(&v));
    normalize(&mut v);
    println!("Magnitude of {v:?} after normalization: {}", magnitude(&v));
}
```

> - 注意在 `normalize` 中可以对每个元素做 `*item /= mag`。这是因为我们用可变引用遍历数组，`for` 循环因此给出每个元素的可变引用。
>
> - 这里也可以接受切片引用，例如 `fn magnitude(vector: &[f64]) -> f64`。函数会更通用，但代价是运行时长度检查。

