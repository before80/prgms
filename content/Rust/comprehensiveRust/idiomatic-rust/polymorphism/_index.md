+++
title = "4 多态"
date = 2026-08-11T11:30:00+08:00
weight = 468
type = "docs"
description = "多态 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism.html)

# 4 多态

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub trait Trait {}

pub struct HasGeneric<T>(T);

pub enum Either<A, B> {
    Left(A),
    Right(B),
}

fn takes_generic<T: Trait>(value: &T) {}

fn takes_dyn(value: &dyn Trait) {}
```

> - Rust 提供了丰富的多态机制，但与其它流行语言的做法有所不同！
>
> - 本章将介绍 Rust 多态的细节，以及它与其它语言的异同。

