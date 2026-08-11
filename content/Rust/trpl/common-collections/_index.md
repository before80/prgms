+++
title = "第8章 常见集合"
date = 2026-08-05T08:44:00+08:00
weight = 33
type = "docs"
description = "介绍向量、字符串与哈希映射等常用标准库集合"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 常见集合 {#common-collections}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch08-00-common-collections.html](https://doc.rust-lang.org/stable/book/ch08-00-common-collections.html)


　　Rust 的标准库包含许多非常有用的数据结构，称为*集合*（collections）。多数其他数据类型表示的是一个具体的值，而集合可以包含多个值。与内置的数组和元组不同，这些集合所指向的数据存放在堆上，因此数据量不必在编译期就知道，并且可以在程序运行时增长或缩小。每种集合都有不同的能力与代价，随着经验积累，你会逐渐学会在当前场景下选择合适的那一种。本章我们讨论 Rust 程序里非常常用的三种集合：

- *向量*（vector）让你可以把数量可变的值彼此相邻地存放。
- *字符串*（string）是字符的集合。我们之前提过 `String` 类型，本章会深入讨论。
- *哈希映射*（hash map）让你把一个值与某个键关联起来。它是更一般的*映射*（map）数据结构的一种具体实现。

　　若要了解标准库提供的其他集合类型，请参阅[文档][collections]。

　　我们将讨论如何创建和更新向量、字符串与哈希映射，以及各自的独特之处。

[collections]: https://doc.rust-lang.org/stable/std/collections/index.html
