+++
title = "4.2.9 Trait 对象的局限"
date = 2026-08-11T11:30:00+08:00
weight = 489
type = "docs"
description = "09-Trait 对象的局限 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/dynamic-dispatch/limits.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/dynamic-dispatch/limits.html)

# 4.2.9 Trait 对象的局限

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::any::Any;

pub trait Trait: Any {}

impl Trait for i32 {}

fn main() {
    dbg!(size_of::<i32>()); // 4 字节，拥有的值
    dbg!(size_of::<&i32>()); // 8 字节，引用
    dbg!(size_of::<&dyn Trait>()); // 16 字节，胖指针
}
```

> - Trait 对象是一种有限的解题方式。
>
> - 若想从 trait 对象向下转型（downcast）到具体类型，需要指定该 trait 以 `Any` 为父 trait，或让 trait 对象同时覆盖主 trait 与 `Any`。
>
>   即便如此，你仍需要把 `dyn MyTrait` 转成 `dyn Any`。
>
> - Trait 对象有内存开销：它们是「胖指针」（wide pointer），不仅要保存数据本身的指针，还要再保存一份虚表指针。
>
> - Trait 对象作为动态大小类型，实际使用时只能通过引用或指针类型。
>
>   使用 trait 对象时，有解引用该值及相关 trait 方法的基线开销。

