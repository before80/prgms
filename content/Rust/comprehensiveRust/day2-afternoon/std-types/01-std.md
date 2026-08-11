+++
title = "3.1 标准库"
date = 2026-08-11T11:30:00+08:00
weight = 103
type = "docs"
description = "01-标准库 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/std-types/std.html](https://google.github.io/comprehensive-rust/std-types/std.html)

# 3.1 标准库

Rust 自带标准库，帮助确立一套 Rust 库与程序共用的类型。这样两个库可以顺利协作，因为它们都使用同一种 `String` 类型。

实际上，Rust 的标准库分好几层：`core`、`alloc` 与 `std`。

- `core` 包含最基本的类型与函数，它们不依赖 `libc`、分配器，甚至不依赖操作系统的存在。
- `alloc` 包含需要全局堆分配器的类型，例如 `Vec`、`Box` 与 `Arc`。
- 嵌入式 Rust 应用通常只用 `core`，有时也会用 `alloc`。
