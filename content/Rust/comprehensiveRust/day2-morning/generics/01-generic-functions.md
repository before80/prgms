+++
title = "4.1 泛型函数"
date = 2026-08-11T11:30:00+08:00
weight = 86
type = "docs"
description = "01-泛型函数 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/generics/generic-functions.html](https://google.github.io/comprehensive-rust/generics/generic-functions.html)

# 4.1 泛型函数

Rust 支持泛型（generics），让你可以对所用或所存的类型抽象算法或数据结构（例如排序或二叉树）。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn pick<T>(cond: bool, left: T, right: T) -> T {
    if cond { left } else { right }
}

fn main() {
    println!("picked a number: {:?}", pick(true, 222, 333));
    println!("picked a string: {:?}", pick(false, 'L', 'R'));
}
```

> - 展示 `pick` 的单态化（monomorphized）版本会有帮助：可以在讲泛型 `pick` 之前展示，以说明泛型如何减少代码重复；也可以在讲完泛型之后展示，以说明单态化如何工作。
>
>   ```rust
>   // Copyright 2023 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   fn pick_i32(cond: bool, left: i32, right: i32) -> i32 {
>       if cond { left } else { right }
>   }
>
>   fn pick_char(cond: bool, left: char, right: char) -> char {
>       if cond { left } else { right }
>   }
>   ```
>
> - Rust 会根据参数与返回值的类型为 `T` 推断类型。
>
> - 本例中我们只用了原始类型 `i32` 与 `char` 作为 `T`，但这里可以用任意类型，包括用户自定义类型：
>
>   ```rust
>   // Copyright 2023 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   struct Foo {
>       val: u8,
>   }
>
>   pick(false, Foo { val: 7 }, Foo { val: 99 });
>   ```
>
> - 这类似 C++ 模板，但 Rust 会立即对泛型函数做部分编译，因此该函数必须对所有满足约束的类型都有效。例如，试着把 `pick` 改成在 `cond` 为假时返回 `left + right`。即便实际只用到整数实例化的 `pick`，Rust 仍认为它无效。C++ 则允许这样做。
>
> - 泛型代码会根据调用点变成非泛型代码。这是零成本抽象：结果与你手写、不带抽象的数据结构完全一样。

