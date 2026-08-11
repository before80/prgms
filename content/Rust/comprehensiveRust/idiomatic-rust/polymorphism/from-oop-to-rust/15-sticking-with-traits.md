+++
title = "4.2.15 可被用户扩展的多态 Trait"
date = 2026-08-11T11:30:00+08:00
weight = 495
type = "docs"
description = "15-可被用户扩展的多态 Trait — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/sticking-with-traits.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/sticking-with-traits.html)

# 4.2.15 可被用户扩展的多态 Trait

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
// Crate A

pub trait Trait {
    fn use_trait(&self) {}
}

// Crate B，依赖 A

pub struct Data(u8);

impl Trait for Data {}

fn main() {
    let data = Data(7u8);
    data.use_trait();
}
```

> - 普通 trait 我们已经讲过很多；与枚举和密封 trait 相比，它们允许用户通过实现 API 所要求的行为来扩展 API。
>
> 这种可扩展性在许多领域都很强大，从序列化到硬件的抽象表示，再到类型安全的线性代数。
>
> - 若 trait 在 crate 中公开暴露，依赖该 crate 的用户就可以为自己定义的类型实现该 trait。

