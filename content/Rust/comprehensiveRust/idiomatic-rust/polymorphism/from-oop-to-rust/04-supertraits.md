+++
title = "4.2.4 Rust 中的「继承」与父 Trait"
date = 2026-08-11T11:30:00+08:00
weight = 484
type = "docs"
description = "04-Rust 中的「继承」与父 Trait — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/supertraits.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/supertraits.html)

# 4.2.4 Rust 中的「继承」与父 Trait

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub trait SuperTrait {}

pub trait Trait: SuperTrait {}
```

> - 在 Rust 中，trait 可以依赖其它 trait。我们已经熟悉 trait 可以有父 trait（supertrait）。
>
> - 表面上看这很像继承。
>
> - 这是一种类似继承的机制，但把数据与行为分开。
>
> - 让行为保持易于推理的状态。
>
> - 也让我们更容易实现「多重继承」想达成的目标：
>
>   我们只关心类型在「明确要求该行为」的那一点上具备什么能力（用 trait 约束泛型时）。
>
>   在泛型上指定多个 trait，就知道该类型拥有所有这些 trait 的方法。
>
> - 不涉及字段继承。Trait 不暴露字段，只暴露方法和关联类型 / 常量。

