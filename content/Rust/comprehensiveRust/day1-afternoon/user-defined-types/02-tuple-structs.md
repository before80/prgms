+++
title = "4.2 元组结构体"
date = 2026-08-11T11:30:00+08:00
weight = 56
type = "docs"
description = "02-元组结构体 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/user-defined-types/tuple-structs.html](https://google.github.io/comprehensive-rust/user-defined-types/tuple-structs.html)

# 4.2 元组结构体

若字段名不重要，可以使用元组结构体（tuple struct）：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
struct Point(i32, i32);

fn main() {
    let p = Point(17, 23);
    println!("({}, {})", p.0, p.1);
}
```

这常用于单字段包装类型（称为 newtype）：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
struct PoundsOfForce(f64);
struct Newtons(f64);

fn compute_thruster_force() -> PoundsOfForce {
    todo!("Ask a rocket scientist at NASA")
}

fn set_thruster_force(force: Newtons) {
    // ……
}

fn main() {
    let force = compute_thruster_force();
    set_thruster_force(force);
}
```

> - Newtype 是在原始类型上编码额外信息的好方法，例如：
>   - 数值带有单位：上例中的 `Newtons`。
>   - 值在创建时已通过校验，后续使用不必再反复验证：如 `PhoneNumber(String)` 或
>     `OddNumber(u32)`。
> - Newtype 模式在
>   [「地道 Rust」模块](../idiomatic/leveraging-the-type-system/newtype-pattern.md)
>   中有更详细的讲解。
> - 演示如何通过访问 newtype 中的唯一字段，把一个 `f64` 加到 `Newtons` 类型上。
>   - Rust 一般避免隐式转换，例如自动解包，或把布尔值当作整数。
>     - 运算符重载会在第 2 天讨论
>       （[标准库 Trait](../std-traits.md)）。
> - 当元组结构体没有字段时，可以省略 `()`。结果是零大小类型（ZST, zero-sized type），该类型只有一个值（即类型名本身）。
>   - 这常见于实现某种行为但不携带数据的类型（例如总是返回 EOF 的 `NullReader`）。
> - 本例隐约呼应
>   [火星气候轨道器](https://en.wikipedia.org/wiki/Mars_Climate_Orbiter)
>   事故。

