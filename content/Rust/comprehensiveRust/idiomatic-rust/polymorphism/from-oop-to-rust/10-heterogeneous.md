+++
title = "4.2.10 异构集合"
date = 2026-08-11T11:30:00+08:00
weight = 490
type = "docs"
description = "10-异构集合 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/dynamic-dispatch/heterogeneous.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/dynamic-dispatch/heterogeneous.html)

# 4.2.10 异构集合

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::fmt::Display;

pub struct Lambda;

impl Display for Lambda {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "λ")
    }
}

fn main() {
    let heterogeneous: Vec<Box<dyn Display>> = vec![
        Box::new(42u32),
        Box::new(String::from("Woah")),
        Box::new(Lambda),
    ];
    for item in heterogeneous {
        // 我们知道 "item" 实现了 Display，但别的一无所知！
        println!("Display output: {}", item);
    }
}
```

> - `dyn Trait` 作为动态分发工具，让我们能在集合中存放异构数据。
>
> - 本例中，我们存放所有实现 `std::fmt::Display` 的类型，并把该集合中的所有项打印到屏幕。

