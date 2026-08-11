+++
title = "4.2.13 密封 Trait"
date = 2026-08-11T11:30:00+08:00
weight = 493
type = "docs"
description = "13-密封 Trait — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/sealed-traits.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/sealed-traits.html)

# 4.2.13 密封 Trait

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
// crate 可以访问 "sealed" 模块及其 trait，但依赖它的项目不能。
mod sealed {
    pub trait Sealed {}
    impl Sealed for String {}
    impl Sealed for Vec<u8> {}
    //...
}

pub trait APITrait: sealed::Sealed {
    /* methods */
}
impl APITrait for String {}
impl APITrait for Vec<u8> {}
```

> - 动机：我们希望在 crate 内使用由 trait 驱动的代码，但不希望依赖该 crate 的项目能够实现某个 trait。
>
> 为什么？
>
> 该 trait 在此时对下游实现而言可能被视为不稳定。
>
> 或者：领域对幼稚的 trait 实现风险很高（例如密码学）。
>
> - 所用机制是限制对某个父 trait 的访问，从而阻止下游用户为其类型实现该 trait。
>
> - 为何不直接用枚举？
>
>   - 枚举会暴露实现细节——「这对这些类型有效」。
>
>   - 用户需要使用枚举的变体构造器才能使用 API。
>
>   - 用户可以在自己的代码中把该枚举当作类型使用；枚举一变，用户就得跟着改代码。
>
>   - 枚举需要按变体分支，而密封 trait 让编译器能为每种类型指定单态化后的函数。

