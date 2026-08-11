+++
title = "第19章 模式与匹配"
date = 2026-08-05T08:44:00+08:00
weight = 90
type = "docs"
description = "模式是 Rust 中用于匹配类型结构的特殊语法，可与 match 等构造配合控制程序流程。"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 模式与匹配 {#patterns-and-matching}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch19-00-patterns.html](https://doc.rust-lang.org/stable/book/ch19-00-patterns.html)


　　**模式**（*pattern*）是 Rust 中一种特殊的语法，用来匹配类型的结构，无论类型简单还是复杂。将模式与 `match` 表达式及其他结构结合使用，可以让你对程序的控制流有更多掌控。模式由以下内容中的某种组合构成：

- 字面值
- 解构后的数组、枚举、结构体或元组
- 变量
- 通配符
- 占位符

　　模式的一些例子包括 `x`、`(a, 3)` 和 `Some(Color::Red)`。在允许使用模式的上下文中，这些组成部分描述了数据的形状。程序随后会让值与模式匹配，以决定它是否具有继续运行某段特定代码所需的数据形状。

　　要使用模式，我们会把它与某个值进行比较。如果模式匹配该值，就能在代码中使用这个值的各个部分。回忆一下第六章讨论 `match` 表达式时用到模式的情形，比如硬币分类器的例子。如果值符合模式的形状，就可以使用其中绑定出来的变量或字段；如果不符合，与该模式关联的代码就不会运行。

　　本章可以视为一份与模式有关内容的参考。我们会介绍哪些位置可以合法使用模式，可反驳（*refutable*）模式与不可反驳（*irrefutable*）模式之间的区别，以及你可能见到的各种模式语法。到本章末尾，你将掌握如何用模式以清晰的方式表达许多概念。
