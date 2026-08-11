+++
title = "2.2 内存管理方式"
date = 2026-08-11T11:30:00+08:00
weight = 125
type = "docs"
description = "02-内存管理方式 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/memory-management/approaches.html](https://google.github.io/comprehensive-rust/memory-management/approaches.html)

# 2.2 内存管理方式

传统上，语言大致分为两大类：

- 通过手动内存管理获得完全控制：C、C++、Pascal……
  - 程序员决定何时在堆上分配或释放内存。
  - 程序员必须判断指针是否仍指向有效内存。
  - 研究表明，程序员会犯错。
- 通过运行时自动内存管理获得完全安全：Java、Python、Go、Haskell……
  - 运行时系统确保内存在仍可被引用时不会被释放。
  - 通常用引用计数或垃圾回收实现。

Rust 提供了一种新的折中：

> 通过在编译期强制正确的内存管理，同时获得完全控制与安全。

它通过显式的所有权（ownership）概念做到这一点。

> 本页旨在帮助来自其他语言的学员把 Rust 放进合适的上下文中。
>
> - C 必须用 `malloc` 与 `free` 手动管理堆。常见错误包括：忘记调用 `free`、对同一指针多次 `free`、或在内存已释放后仍解引用指针。
>
> - C++ 有智能指针（`unique_ptr`、`shared_ptr`）等工具，利用语言对析构函数调用的保证，在函数返回时释放内存。但这些工具仍然很容易误用，从而产生与 C 类似的 bug。
>
> - Java、Go 与 Python 依赖垃圾回收器识别不再可达的内存并丢弃。这保证了任意指针都可以解引用，消除了 use-after-free 等一类 bug。但 GC 有运行时开销，且难以调优。
>
> Rust 的所有权与借用（borrowing）模型在许多情况下能达到接近 C 的性能——分配与释放恰好发生在需要之处，零额外成本。它也提供类似 C++ 智能指针的工具。需要时还有引用计数等选项，甚至有 crate 支持运行时垃圾回收（本课程不覆盖）。

