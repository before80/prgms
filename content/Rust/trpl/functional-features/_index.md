+++
title = "第13章 函数式语言特性：迭代器与闭包"
date = 2026-08-05T08:44:00+08:00
weight = 56
type = "docs"
description = "介绍闭包与迭代器等受函数式编程启发的 Rust 特性"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 函数式语言特性：迭代器与闭包 {#functional-language-features-iterators-and-closures}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch13-00-functional-features.html](https://doc.rust-lang.org/stable/book/ch13-00-functional-features.html)


　　Rust 的设计从许多既有语言与技术中汲取灵感，其中一个重要影响来自*函数式编程*（functional programming）。函数式风格常常把函数当作值来用：作为参数传入、从其他函数返回、赋给变量以便稍后执行，等等。

　　本章不会争论“什么算或不算函数式编程”，而是讨论 Rust 中与许多常被称为函数式语言的特性相似的部分。

　　更具体地说，我们将涵盖：

- *闭包*（closure）：一种可以存进变量的、类似函数的构造
- *迭代器*（iterator）：处理一系列元素的方式
- 如何用闭包和迭代器改进第 12 章的 I/O 项目
- 闭包与迭代器的性能（剧透：它们比你以为的更快！）

　　我们此前已经讲过一些同样受函数式风格影响的 Rust 特性，例如模式匹配和枚举。掌握闭包和迭代器是写出快速、地道的 Rust 代码的重要一环，因此整章都会围绕它们展开。
