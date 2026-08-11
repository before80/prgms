+++
title = "4.1.9 静态大小与动态大小类型"
date = 2026-08-11T11:30:00+08:00
weight = 478
type = "docs"
description = "09-静态大小与动态大小类型 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/sized.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/sized.html)

# 4.1.9 静态大小与动态大小类型

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::fmt::Debug;

pub struct AlwaysSized<T /* : Sized */>(T);

pub struct OptionallySized<T: ?Sized>(T);

type Dyn1 = OptionallySized<dyn Debug>;
```

> - 动机：能够区分「大小在编译期已知」与「大小在运行时已知」的类型，是有用的。
>
> - `Sized` trait 会由编译期大小已知的类型自动实现。
>
>   该 trait 也会自动加到未选择退出 sized 的任意类型参数上。
>
> - 大多数类型实现 `Sized`：它们在编译期有已知大小。
>
>   `[T]`、`str` 和 `dyn Trait` 等都是动态大小类型（DST）。它们的大小作为该类型值的引用的一部分存储。
>
> - 除非另行指定，类型参数会自动实现 `Sized`。
>
> 参考：
>
> - https://doc.rust-lang.org/stable/reference/dynamically-sized-types.html#r-dynamic-sized

