+++
title = "4.2.11 `Any` Trait"
date = 2026-08-11T11:30:00+08:00
weight = 491
type = "docs"
description = "11-`Any` Trait — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/dynamic-dispatch/any-trait.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/dynamic-dispatch/any-trait.html)

# 4.2.11 `Any` Trait

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::any::Any;

#[derive(Debug)]
pub struct ThisImplementsAny;

fn take_any<T: Any>(t: &T) {}

fn main() {
    let is_an_any = ThisImplementsAny;
    take_any(&is_an_any);

    let dyn_any: &dyn Any = &is_an_any;
    dbg!(dyn_any.type_id());
    dbg!(dyn_any.is::<ThisImplementsAny>());
    let is_downcast: Option<&ThisImplementsAny> = dyn_any.downcast_ref();
    dbg!(is_downcast);
}
```

> - `Any` trait 让我们能把 dyn 值向下转型回具体值。
>
> - 这是一个自动 trait（auto trait）：像 Send/Sync/Sized 一样，对满足特定条件的任意类型自动实现。
>
> - `Any` 的条件是类型为 `'static`。也就是说，类型内部不包含任何非 `'static` 的生命周期。
>
> - `Any` 提供两类相关行为：向下转型，以及运行时检查类型是否相同。
>
>   上例中，我们看到可以从 `Any` 自动向下转型到 `ThisImplementsAny`。
>
>   也看到用 `Any::is` 检查值是什么类型。
>
> - `Any` 并不为类型实现反射；你能做的就这些。

