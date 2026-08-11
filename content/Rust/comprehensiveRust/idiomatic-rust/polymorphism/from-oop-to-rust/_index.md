+++
title = "4.2 从 OOP 到 Rust"
date = 2026-08-11T11:30:00+08:00
weight = 480
type = "docs"
description = "从 OOP 到 Rust — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust.html)

# 4.2 从 OOP 到 Rust

- 继承是 OOP 作为范式取得成功的关键。数十年来，大量成功的软件工程以继承作为业务逻辑的核心。

- 那么 Rust 为何回避继承？

- 我们如何从基于继承的解题方式转向 Rust 的做法？

- 在 Rust 中如何表示异构集合？

> - 本节将讨论：如何从 Java、C++ 等 OOP 语言中「用类型做多态解题」的思路，转向 Rust 基于 trait 的多态方式。
>
> - 会有差异，但也有许多共通之处——尤其是与现代 OOP 开发标准相比。请保持开放心态。

