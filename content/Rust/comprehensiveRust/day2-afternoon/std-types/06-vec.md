+++
title = "3.6 `Vec`"
date = 2026-08-11T11:30:00+08:00
weight = 108
type = "docs"
description = "06-`Vec` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/std-types/vec.html](https://google.github.io/comprehensive-rust/std-types/vec.html)

# 3.6 `Vec`

[`Vec`][1] 是标准的可调整大小、堆分配缓冲区：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let mut v1 = Vec::new();
    v1.push(42);
    println!("v1: len = {}, capacity = {}", v1.len(), v1.capacity());

    let mut v2 = Vec::with_capacity(v1.len() + 1);
    v2.extend(v1.iter());
    v2.push(9999);
    println!("v2: len = {}, capacity = {}", v2.len(), v2.capacity());

    // 用元素初始化向量的标准宏。
    let mut v3 = vec![0, 0, 1, 2, 3, 4];

    // 只保留偶数元素。
    v3.retain(|x| x % 2 == 0);
    println!("{v3:?}");

    // 去除连续重复项。
    v3.dedup();
    println!("{v3:?}");
}
```

`Vec` 实现了 [`Deref<Target = [T]>`][2]，这意味着你可以在 `Vec` 上调用切片方法。

[1]: https://doc.rust-lang.org/std/vec/struct.Vec.html
[2]: https://doc.rust-lang.org/std/vec/struct.Vec.html#deref-methods-%5BT%5D

> - `Vec` 与 `String`、`HashMap` 一样是一种集合。它包含的数据存储在堆上。这意味着数据量不必在编译期已知，运行时可增可减。
> - 注意 `Vec<T>` 也是泛型类型，但不必显式指定 `T`。与 Rust 类型推断一贯做法一样，`T` 在第一次 `push` 调用时就确定了。
> - `vec![...]` 是替代 `Vec::new()` 的标准宏，并支持向向量添加初始元素。
> - 用 `[` `]` 索引向量，但越界会 panic。或者用 `get` 会返回 `Option`。`pop` 函数会移除最后一个元素。

