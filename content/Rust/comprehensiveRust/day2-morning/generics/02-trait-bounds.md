+++
title = "4.2 Trait 约束"
date = 2026-08-11T11:30:00+08:00
weight = 87
type = "docs"
description = "02-Trait 约束 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/generics/trait-bounds.html](https://google.github.io/comprehensive-rust/generics/trait-bounds.html)

# 4.2 Trait 约束

使用泛型时，常常希望要求类型实现某个 trait，以便调用该 trait 的方法。

可以用 `T: Trait` 做到：

```rust
// Copyright 2022 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn duplicate<T: Clone>(a: T) -> (T, T) {
    (a.clone(), a.clone())
}

struct NotCloneable;

fn main() {
    let foo = String::from("foo");
    let pair = duplicate(foo);
    println!("{pair:?}");
}
```

> - 试着构造一个 `NotCloneable` 并传给 `duplicate`。
>
> - 需要多个 trait 时，用 `+` 连接它们。
>
> - 演示 `where` 子句，学员读代码时会遇到。
>
>   ```rust
>   // Copyright 2022 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   fn duplicate<T>(a: T) -> (T, T)
>   where
>       T: Clone,
>   {
>       (a.clone(), a.clone())
>   }
>   ```
>
>   - 参数很多时，它能让函数签名更清爽。
>   - 它还有额外能力，因此更强大。
>     - 若有人问起，额外能力是「`:` 左侧的类型可以是任意的」，例如 `Option<T>`。
>
> - 注意 Rust（目前）不支持特化（specialization）。例如，给定原来的 `duplicate`，再增加一个特化的 `duplicate(a: u32)` 是无效的。

