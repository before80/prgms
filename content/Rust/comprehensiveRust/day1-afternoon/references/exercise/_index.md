+++
title = "3.6 练习：几何"
date = 2026-08-11T11:30:00+08:00
weight = 52
type = "docs"
description = "练习：几何 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/references/exercise.html](https://google.github.io/comprehensive-rust/references/exercise.html)

# 3.6 练习：几何

我们将编写几个三维几何的工具函数，用 `[f64;3]` 表示点。函数签名由你自行确定。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
// 计算向量的模长：对各坐标平方求和再开方。
// 用 `sqrt()` 方法求平方根，例如 `v.sqrt()`。

fn magnitude(...) -> f64 {
    todo!()
}

// 归一化向量：先算模长，再把所有坐标除以该模长。

fn normalize(...) {
    todo!()
}

// 用下面的 `main` 测试你的实现。

fn main() {
    println!("Magnitude of a unit vector: {}", magnitude(&[0.0, 1.0, 0.0]));

    let mut v = [1.0, 2.0, 9.0];
    println!("Magnitude of {v:?}: {}", magnitude(&v));
    normalize(&mut v);
    println!("Magnitude of {v:?} after normalization: {}", magnitude(&v));
}
```
