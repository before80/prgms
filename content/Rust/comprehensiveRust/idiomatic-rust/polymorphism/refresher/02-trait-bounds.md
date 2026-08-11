+++
title = "4.1.2 Trait 约束"
date = 2026-08-11T11:30:00+08:00
weight = 471
type = "docs"
description = "02-Trait 约束 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/trait-bounds.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/trait-bounds.html)

# 4.1.2 Trait 约束

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::fmt::Display;

fn print_with_length<T: Display>(item: T) {
    println!("Item: {}", item);
    println!("Length: {}", item.to_string().len());
}

fn main() {
    let number = 42;
    let text = "Hello, Rust!";

    print_with_length(number); // 可用于整数
    print_with_length(text); // 可用于字符串
}
```

> - Trait 最常见的用途，是作为函数或方法上泛型类型参数的约束（bound）。
>
>   若泛型类型参数没有 trait 约束，我们就没有任何可用行为来编写函数和方法。
>
>   Trait 约束让我们能指定：类型要在泛型代码中工作，至少需要具备哪些行为。
>
> 参考：
>
> - https://doc.rust-lang.org/reference/trait-bounds.html

