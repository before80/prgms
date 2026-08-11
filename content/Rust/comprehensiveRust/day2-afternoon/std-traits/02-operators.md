+++
title = "4.2 运算符"
date = 2026-08-11T11:30:00+08:00
weight = 114
type = "docs"
description = "02-运算符 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/std-traits/operators.html](https://google.github.io/comprehensive-rust/std-traits/operators.html)

# 4.2 运算符

运算符重载通过 [`std::ops`][1] 中的 trait 实现：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug, Copy, Clone)]
struct Point {
    x: i32,
    y: i32,
}

impl std::ops::Add for Point {
    type Output = Self;

    fn add(self, other: Self) -> Self {
        Self { x: self.x + other.x, y: self.y + other.y }
    }
}

fn main() {
    let p1 = Point { x: 10, y: 20 };
    let p2 = Point { x: 100, y: 200 };
    println!("{p1:?} + {p2:?} = {:?}", p1 + p2);
}
```

> 讨论点：
>
> - 你可以为 `&Point` 实现 `Add`。什么情况下有用？
>   - 答：`Add::add` 会消费 `self`。若你为之重载运算符的类型 `T` 不是 `Copy`，也应考虑为 `&T` 重载运算符。这样可避免调用点不必要的克隆。
> - 为什么 `Output` 是关联类型？能否做成方法的类型参数？
>   - 简答：函数类型参数由调用方控制，但关联类型（如 `Output`）由 trait 的实现方控制。
> - 可以为两个不同类型实现 `Add`，例如 `impl Add<(i32, i32)> for Point` 会把元组加到 `Point` 上。
>
> `Not` trait（`!` 运算符）值得注意：它不会像 C 系语言的同名运算符那样把参数转成 `bool`；对整数类型，它会翻转数字的每一位，在算术上等价于用 `-1` 减去参数：`!5 == -6`。


[1]: https://doc.rust-lang.org/std/ops/index.html
