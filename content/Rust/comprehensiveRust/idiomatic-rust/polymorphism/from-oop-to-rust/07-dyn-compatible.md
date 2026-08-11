+++
title = "4.2.7 Dyn 兼容性"
date = 2026-08-11T11:30:00+08:00
weight = 487
type = "docs"
description = "07-Dyn 兼容性 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/dynamic-dispatch/dyn-compatible.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/dynamic-dispatch/dyn-compatible.html)

# 4.2.7 Dyn 兼容性

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub trait Trait {
    // dyn 兼容
    fn takes_self(&self);

    // dyn 兼容，但在 dyn 时不能使用此方法
    fn takes_self_and_param<T>(&self, input: &T);

    // 不再 dyn 兼容
    const ASSOC_CONST: i32;

    // 不再 dyn 兼容
    fn clone(&self) -> Self;
}
```

> - 并非所有 trait 都能作为 trait 对象来调用。能这样调用的 trait 称为 *dyn 兼容*（dyn compatible）的 trait。
>
> - 这以前叫 *对象安全的 trait*（object safe traits）或 *对象安全*（object safety）。
>
> - 动态分发把大量编译期类型信息卸载到运行时的虚表信息中。
>
>   若某个概念无法有意义地存入虚表，要么该 trait 不再 dyn 兼容，要么那些方法被排除在 dyn 上下文之外。
>
> - 当某 trait 的所有父 trait 都 dyn 兼容，且没有关联常量/类型、也没有依赖泛型的方法时，该 trait 是 dyn 兼容的。
>
> - 你最常遇到 dyn 不兼容的 trait，是因为它们有关联类型/常量，或返回 `Self`（例如 Clone trait 不是 dyn 兼容的）。
>
>   因为关联数据必须存进虚表，会占用额外内存。
>
>   对于像 `clone` 这样的方法，返回类型取决于 `self` 的具体类型，因此取消了 dyn 兼容性。
>
> 参考：
>
> - https://doc.rust-lang.org/1.91.1/reference/items/traits.html#r-items.traits.dyn-compatible

