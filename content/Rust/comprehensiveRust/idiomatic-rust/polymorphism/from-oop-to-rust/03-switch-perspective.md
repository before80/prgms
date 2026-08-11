+++
title = "4.2.3 从 Rust 视角看继承"
date = 2026-08-11T11:30:00+08:00
weight = 483
type = "docs"
description = "03-从 Rust 视角看继承 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/switch-perspective.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/switch-perspective.html)

# 4.2.3 从 Rust 视角看继承

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
// 数据
pub struct Data {
    id: usize,
    name: String,
}

// 具体行为
impl Data {
    fn new(id: usize, name: impl Into<String>) -> Self {
        Self { id, name: name.into() }
    }
}

// 抽象行为
trait Named {
    fn name(&self) -> &str;
}

// 实例化的行为
impl Named for Data {
    fn name(&self) -> &str {
        &self.name
    }
}
```

> - 从 Rust 的视角——一个从未有过继承的世界——引入继承会像是在类型与 trait 之间搅浑水。
>
> - 类型是具体的数据及其关联行为。
>
>   Trait 是必须由类型实现的抽象行为。
>
>   类则是数据、行为，以及对这些行为的覆盖的组合。
>
> - 站在 Rust 这边看，可继承的类像是「既是类型又是 trait」。
>
> - 这并不是优点，因为我们再也无法清晰地推理具体类型。
>
> - 无法把二者分开时，就很难区分「泛型行为」与「具体细节」，因为在 OOP 里这两个概念缠在一起。
>
> - 扁平字段访问与类型定义中 DRY 的便利，抵不上在编写代码时无法明确区分行为与数据所带来的损失。

