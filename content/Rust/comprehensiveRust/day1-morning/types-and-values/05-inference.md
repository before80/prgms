+++
title = "3.5 类型推断"
date = 2026-08-11T11:30:00+08:00
weight = 21
type = "docs"
description = "05-类型推断 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/types-and-values/inference.html](https://google.github.io/comprehensive-rust/types-and-values/inference.html)

# 3.5 类型推断

Rust 会根据变量的 _用法_ 来确定类型：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn takes_u32(x: u32) {
    println!("u32: {x}");
}

fn takes_i8(y: i8) {
    println!("i8: {y}");
}

fn main() {
    let x = 10;
    let y = 20;

    takes_u32(x);
    takes_i8(y);
    // takes_u32(y);
}
```

> 本页演示 Rust 编译器如何根据变量声明与用法给出的约束来推断类型。
>
> 务必强调：这样声明的变量并不是某种可容纳任意数据的动态“任意类型”。此类声明生成的机器码
> 与显式声明类型时完全相同。编译器替我们完成工作，帮助我们写出更简洁的代码。
>
> 当没有任何约束限制整数字面量的类型时，Rust 默认使用 `i32`。这有时会在错误信息中显示为
> `{integer}`。类似地，浮点字面量默认使用 `f64`。
>
> ```rust
> // Copyright 2023 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> fn main() {
>     let x = 3.14;
>     let y = 20;
>     assert_eq!(x, y);
>     // 错误：没有为 `{float} == {integer}` 实现
> }
> ```

