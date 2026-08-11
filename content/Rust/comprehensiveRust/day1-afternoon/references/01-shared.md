+++
title = "3.1 共享引用"
date = 2026-08-11T11:30:00+08:00
weight = 47
type = "docs"
description = "01-共享引用 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/references/shared.html](https://google.github.io/comprehensive-rust/references/shared.html)

# 3.1 共享引用

引用提供了在不取得所有权（ownership）的情况下访问另一个值的方式，也称为“借用”（borrowing）。共享引用是只读的，被引用的数据不能被修改。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let a = 'A';
    let b = 'B';

    let mut r: &char = &a;
    dbg!(r);

    r = &b;
    dbg!(r);
}
```

指向类型 `T` 的共享引用类型为 `&T`。用 `&` 运算符创建引用值。`*` 运算符“解引用”一个引用，得到其值。

> - Rust 中的引用永远不会为 null，因此无需做空指针检查。
>
> - 常说引用“借用”了它所指向的值；对不熟悉指针的学员，这是个很好的模型：代码可以用引用访问该值，但值仍由原变量“拥有”。课程会在第 3 天更详细地讨论所有权。
>
> - 引用以指针实现，一个关键优势是它们可以远小于所指向的对象。熟悉 C 或 C++ 的学员会把引用看作指针。课程后续会讲解 Rust 如何防止使用原始指针带来的内存安全问题。
>
> - 除了调用方法时 Rust 会自动引用与解引用外，通常需要用 `&` 显式取引用。
>
> - 在某些情况下 Rust 会自动解引用，尤其是调用方法时（试试 `r.is_ascii()`）。不需要像 C++ 那样的 `->` 运算符。
>
> - 本例中 `r` 是可变的，因此可以重新赋值（`r = &b`）。注意这是重新绑定 `r`，让它指向别的东西。这与 C++ 不同：在 C++ 中对引用赋值会改变被引用的值。
>
> - 即使被引用的值本身是可变的，共享引用也不允许修改它。试试 `*r = 'X'`。
>
> - Rust 会跟踪所有引用的生命周期（lifetime），确保它们足够长。安全 Rust 中不会出现悬垂引用。
>
> - 讲到所有权时，我们会更多讨论借用以及如何防止悬垂引用。

