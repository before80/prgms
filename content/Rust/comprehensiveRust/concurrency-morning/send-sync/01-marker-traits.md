+++
title = "4.1 标记 Trait"
date = 2026-08-11T11:30:00+08:00
weight = 353
type = "docs"
description = "01-标记 Trait — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/send-sync/marker-traits.html](https://google.github.io/comprehensive-rust/concurrency/send-sync/marker-traits.html)

# 4.1 标记 Trait

Rust 如何禁止跨线程共享访问？答案在两个 trait 中：

- [`Send`][1]：若把 `T` 移过线程边界是安全的，则类型 `T` 是 `Send`。
- [`Sync`][2]：若把 `&T` 移过线程边界是安全的，则类型 `T` 是 `Sync`。

`Send` 与 `Sync` 是 [unsafe trait][3]。只要类型只包含 `Send` 与 `Sync` 类型，编译器会自动为你派生它们。在你知道这样做有效时，也可以手动实现它们。

[1]: https://doc.rust-lang.org/std/marker/trait.Send.html
[2]: https://doc.rust-lang.org/std/marker/trait.Sync.html
[3]: ../../unsafe-rust/unsafe-traits.md

> - 可以把这些 trait 看作标记：该类型具有某些线程安全属性。
> - 它们可以像普通 trait 一样用在泛型约束中。

