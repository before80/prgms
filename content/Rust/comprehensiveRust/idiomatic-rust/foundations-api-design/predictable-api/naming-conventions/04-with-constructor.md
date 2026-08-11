+++
title = "2.2.1.4 With：构造函数"
date = 2026-08-11T11:30:00+08:00
weight = 404
type = "docs"
description = "04-With：构造函数 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/with-constructor.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/with-constructor.html)

# 2.2.1.4 With：构造函数

作为构造函数的 `with`，在其余使用默认值的同时设置类型的某一个值。

`with` 意为“带有特定设置的 `<Type>`”。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
impl<T> Vec<T> {
    // 为至少 N 个元素初始化内存，len 仍为 0。
    fn with_capacity(capacity: usize) -> Vec<T>;
}
```

> - `with` 可作为构造函数前缀出现，最常见于为容器类型初始化堆内存。
>
>   这种情况下，它与 `new` 构造函数不同，因为它指定了 API 用户通常不关心的某个值。
>
> - 问问学员：为何不用 `from_capacity`？
>
>   答案：`Vec::with_capacity` 作为方法调用，读起来像创建“带有容量的 Vec”。考虑 `Vec::new_capacity` 或 `Vec::from_capacity` 写下来时如何扫读——它们并不能很好地传达在做什么。

