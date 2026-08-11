+++
title = "4.2.14 用枚举密封"
date = 2026-08-11T11:30:00+08:00
weight = 494
type = "docs"
description = "14-用枚举密封 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/sealing-with-enums.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/sealing-with-enums.html)

# 4.2.14 用枚举密封

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::collections::BTreeMap;
pub enum GetSource {
    WebUrl(String),
    BytesMap(BTreeMap<String, Vec<u8>>),
}

impl GetSource {
    fn get(&self, url: &str) -> Option<&Vec<u8>> {
        match self {
            Self::WebUrl(source) => unimplemented!(),
            Self::BytesMap(map) => map.get(url),
        }
    }
}
```

> - 动机：API 围绕一份有效类型列表设计，不期望 API 用户扩展它。
>
> - Rust 中的枚举是 *代数数据类型*（algebraic data types），我们可以为每个变体定义不同的结构。
>
>   对某些领域，这可能已是足够的多态。多试验，看什么管用、哪种方案更合理。
>
> - 让面向用户的 API 部分引用某个枚举，用户就知道哪些类型是有效输入，并能用可用的方法构造这些类型。
>
>   - 若组成枚举的类型有 API 内部维护的不变量，且用户构造这些类型的唯一途径是通过构建并维护这些不变量的构造器，那么你就可以确信泛型方法的输入满足其不变量。
>
>   - 若组成枚举的类型反而是用户可自由构造的，则可能需要考虑净化与解释。

