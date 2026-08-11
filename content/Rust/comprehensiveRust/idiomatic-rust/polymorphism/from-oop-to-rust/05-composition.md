+++
title = "4.2.5 组合优于继承"
date = 2026-08-11T11:30:00+08:00
weight = 485
type = "docs"
description = "05-组合优于继承 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/composition.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/composition.html)

# 4.2.5 组合优于继承

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub struct Uuid([u8; 16]);

pub struct Address {
    street: String,
    city_or_province: String,
    code: String,
    country: String,
}

pub struct User {
    id: Uuid,
    address: Address,
}
```

> - 我们不用 mixin 或继承，而是通过创建不同类型的字段来组合类型。
>
>   这有缺点，主要是字段访问的人体工学，但给了开发者对「类型做什么、能访问什么」很大的控制力与清晰度。
>
> - 派生 trait 时，确保结构体的所有字段类型或枚举的所有变体类型都实现了该 trait。Derive 宏往往假定组成新类型的所有类型都已实现该 trait。

