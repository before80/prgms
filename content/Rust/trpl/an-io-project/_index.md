+++
title = "第12章 I/O 项目：构建命令行程序"
date = 2026-08-05T08:44:00+08:00
weight = 49
type = "docs"
description = "回顾已学知识，并用标准库构建命令行搜索工具 minigrep"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# I/O 项目：构建命令行程序 {#an-i-o-project-building-a-command-line-program}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch12-00-an-io-project.html](https://doc.rust-lang.org/stable/book/ch12-00-an-io-project.html)


　　本章既是对目前所学诸多技能的回顾，也会继续探索一些标准库功能。我们将构建一个与文件和命令行输入/输出交互的命令行工具，借此练习你已经掌握的 Rust 概念。

　　Rust 速度快、内存安全、能产出单一二进制文件，并且跨平台支持出色，非常适合编写命令行工具。因此在本项目中，我们会实现经典命令行搜索工具 `grep`（**g**lobally search a **r**egular **e**xpression and **p**rint）的简化版。最简单的用法是：`grep` 在指定文件中搜索指定字符串。为此，它接收文件路径和字符串作为参数，然后读取文件，找出包含该字符串的行，并打印这些行。

　　过程中，我们还会演示如何让命令行工具使用许多同类工具都会用到的终端特性：读取环境变量以便用户配置行为；把错误信息打印到标准错误流（`stderr`）而不是标准输出（`stdout`），这样用户就可以把成功输出重定向到文件，同时仍在屏幕上看到错误信息。

　　Rust 社区成员 Andrew Gallant 已经写出了功能完备、速度极快的 `grep` 实现，名为 `ripgrep`。相比之下，我们的版本会相当简单，但本章会为你理解像 `ripgrep` 这样的真实项目打下一些必要的背景知识。

　　我们的 `grep` 项目将综合运用此前学过的多个概念：

- 组织代码（[第 7 章][ch7]）
- 使用向量与字符串（[第 8 章][ch8]）
- 错误处理（[第 9 章][ch9]）
- 在合适的地方使用特征（trait）与生命周期（[第 10 章][ch10]）
- 编写测试（[第 11 章][ch11]）

　　我们还会简要介绍闭包（closure）、迭代器（iterator）和特征对象（trait object），这些内容将在 [第 13 章][ch13] 和 [第 18 章][ch18] 中详细讲解。

[ch7]: ../modules/
[ch8]: ../common-collections/
[ch9]: ../error-handling/
[ch10]: ../generics/
[ch11]: ../testing/
[ch13]: ../functional-features/
[ch18]: ../oop/
