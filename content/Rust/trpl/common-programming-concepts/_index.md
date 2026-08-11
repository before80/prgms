+++
title = "第3章 通用编程概念"
date = 2026-08-05T08:44:00+08:00
weight = 9
type = "docs"
description = "变量、类型、函数、注释与控制流等基础概念"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 通用编程概念 {#common-programming-concepts}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch03-00-common-programming-concepts.html](https://doc.rust-lang.org/stable/book/ch03-00-common-programming-concepts.html)


　　本章介绍几乎每种编程语言都会出现的概念，以及它们在 Rust 中如何工作。许多编程语言在核心层面有许多共同点。本章呈现的概念没有一个是 Rust 独有的，但我们会在 Rust 的语境中讨论它们，并说明使用时的约定。

　　具体来说，你会学到变量、基本类型、函数、注释和控制流。这些基础会出现在每一个 Rust 程序中，尽早掌握它们能给你一个扎实的起点。

> #### 关键字
>
> 与许多其他语言一样，Rust 语言有一组保留给语言本身使用的*关键字*（keywords）。请记住，你不能用这些词作为变量或函数的名称。大多数关键字有特殊含义，你会用它们在 Rust 程序中完成各种任务；少数当前没有关联功能，但被保留以备将来可能加入的功能。关键字列表见[附录 A][appendix_a]。

[appendix_a]: ../appendix/01-a-keywords/
