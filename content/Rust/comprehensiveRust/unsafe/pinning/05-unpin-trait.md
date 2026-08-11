+++
title = "8.5 `Unpin` trait（可解除固定）"
date = 2026-08-11T11:30:00+08:00
weight = 551
type = "docs"
description = "05-`Unpin` trait（可解除固定） — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/unpin-trait.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/unpin-trait.html)

# 8.5 `Unpin` trait（可解除固定）

- `Unpin` 类型即使被 `Pin` 包装也可以自由移动
- 大多数类型都实现 `Unpin`，因为它是「`auto trait`」
- `auto trait` 的行为可以更改：
  - `!Unpin` 类型绝不能移动
  - 包含 `PhantomPinned` 字段的类型默认不实现 `Unpin`

> 说明：当某个类型实现了 `Unpin` 时，不会触发 `Pin<Ptr>` 的 pinning 行为。该值可以自由移动。
>
> 说明：几乎所有类型都实现 `Unpin`；由编译器自动实现。
>
> 实现 `Unpin` 的类型相当于声明：「我保证没有自引用，因此移动我总是安全的。」
>
> 问：哪些类型可能是 `!Unpin`？
>
> - 编译器生成的 future
> - 包含 `PhantomPinned` 字段的类型
> - 某些包装 C++ 对象的类型
>
> `!Unpin` 类型一旦被固定就不能再移动


[`PhantomPinned`]: https://doc.rust-lang.org/std/marker/struct.PhantomPinned.html
