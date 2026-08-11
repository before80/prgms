+++
title = "第20章 高级特性"
date = 2026-08-05T08:44:00+08:00
weight = 94
type = "docs"
description = "介绍不安全 Rust、高级 trait 与类型、函数指针与闭包，以及宏等不常用但重要的语言特性。"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 高级特性 {#advanced-features}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch20-00-advanced-features.html](https://doc.rust-lang.org/stable/book/ch20-00-advanced-features.html)


　　现在你已经学会了 Rust 编程语言中最常用的那些部分。在第二十一章再做一个项目之前，我们先来看语言中的一些方面：你可能偶尔会遇到它们，但未必会天天使用。你可以把这一章当作在遇到陌生内容时的参考。本章介绍的这些特性只会在非常特定的场景下派上用场。虽然你可能不会经常用到它们，但我们仍希望确保你了解 Rust 所提供的全部特性。

　　本章将涉及如下内容：

- 不安全 Rust：如何在特定场景下绕过 Rust 的部分安全保证，并自行承担维持这些保证的责任
- 高级 trait：关联类型、默认类型参数、完全限定语法、超 trait，以及与 trait 相关的 newtype 模式
- 高级类型：关于 newtype 模式的更多内容、类型别名、never 类型以及动态大小类型
- 高级函数和闭包：函数指针和返回闭包
- 宏：在编译时定义“用来定义更多代码的代码”的方式

　　这是一组包罗万象的 Rust 特性，总有一些内容会对你有用！让我们开始吧！
