+++
title = "4.5 `impl Trait`"
date = 2026-08-11T11:30:00+08:00
weight = 90
type = "docs"
description = "05-`impl Trait` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/generics/impl-trait.html](https://google.github.io/comprehensive-rust/generics/impl-trait.html)

# 4.5 `impl Trait`

与 trait 约束类似，`impl Trait` 语法可用在函数参数与返回值中：

```rust
// Copyright 2022 Google LLC
// SPDX-License-Identifier: Apache-2.0
// 以下写法的语法糖：
//   fn add_42_millions<T: Into<i32>>(x: T) -> i32 {
fn add_42_millions(x: impl Into<i32>) -> i32 {
    x.into() + 42_000_000
}

fn pair_of(x: u32) -> impl std::fmt::Debug {
    (x + 1, x - 1)
}

fn main() {
    let many = add_42_millions(42_i8);
    dbg!(many);
    let many_more = add_42_millions(10_000_000);
    dbg!(many_more);
    let debuggable = pair_of(27);
    dbg!(debuggable);
}
```

> `impl Trait` 让你能使用无法命名的类型。在不同位置，`impl Trait` 的含义略有不同。
>
> - 作为参数时，`impl Trait` 像带 trait 约束的匿名泛型参数。
>
> - 作为返回类型时，它表示返回类型是某个实现了该 trait 的具体类型，但不写出类型名。当你不想在公共 API 中暴露具体类型时，这很有用。
>
>   返回位置的类型推断比较难。返回 `impl Foo` 的函数自行选定具体返回类型，而不在源码中写出。返回泛型类型（如 `collect<B>() -> B`）的函数可以返回任何满足 `B` 的类型，调用方可能需要选择一个，例如用 `let x: Vec<_> = foo.collect()` 或 turbofish：`foo.collect::<Vec<_>>()`。
>
> `debuggable` 的类型是什么？试着写 `let debuggable: () = ..` 看看错误信息显示什么。

