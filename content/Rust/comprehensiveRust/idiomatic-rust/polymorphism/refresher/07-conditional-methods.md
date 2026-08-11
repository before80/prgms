+++
title = "4.1.7 条件方法"
date = 2026-08-11T11:30:00+08:00
weight = 476
type = "docs"
description = "07-条件方法 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/conditional-methods.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/conditional-methods.html)

# 4.1.7 条件方法

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
// 类型定义上不加 trait 约束。
pub struct Value<T>(T);

// 约束放在该类型的实现上。
impl<T: std::fmt::Display> Value<T> {
    fn log(&self) {
        println!("{}", self.0);
    }
}

// 另一种写法
impl<T> Value<T> {
    // 在 where 表达式中指定 trait 约束
    fn log_error(&self)
    where
        T: std::error::Error,
    {
        eprintln!("{}", self.0);
    }
}
```

> - 编写带泛型参数的类型时，可以为该类型写出依赖参数本身或其实现哪些 trait 的实现。
>
> - 只有当类型满足这些条件时，这些方法才可用。
>
> - 对于有序集合这类希望内部类型始终为 `Ord` 的场景，在类型参数上用这种方式加 trait 约束是首选做法。
>
>   我们不把约束写在类型定义本身上，否则凡是带着泛型参数提到该类型的地方都会引发下游问题。
>
>   用条件方法实现，同样可以很好地维护不变量。

