+++
title = "4.2.6 Trait 对象与动态分发"
date = 2026-08-11T11:30:00+08:00
weight = 486
type = "docs"
description = "06-Trait 对象与动态分发 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/dynamic-dispatch/dyn-trait.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/dynamic-dispatch/dyn-trait.html)

# 4.2.6 Trait 对象与动态分发

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub trait Trait {}

impl Trait for i32 {}
impl Trait for String {}

fn main() {
    let int: &dyn Trait = &42i32;
    let string: &dyn Trait = &String::from("Hello dyn!");;
}
```

> - 动态分发是面向对象编程中的工具，常用于更关心类型行为而非类型本身是什么的场景。
>
>   在 OOP 语言中，动态分发往往是 *隐式* 过程，无法选择退出。
>
>   在 Rust 中，我们使用 `dyn Trait`：一种可选择启用的动态分发形式。
>
> - 对任何 *dyn 兼容*（dyn compatible）的 trait，都可以把对该 trait 实现者的引用强制转换（coerce）为 `dyn Trait` 值。
>
> - 我们称之为 *trait 对象*。其具体类型在编译期未知，但行为已知：即 trait 本身所规定的实现。
>
> - 当你 *需要* OOP 风格的异构数据结构时，可以求助于 `Box<dyn Trait>`，但请优先保持同构并以泛型为基础！

