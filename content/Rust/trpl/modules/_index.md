+++
title = "第7章 包、Crate 与模块"
date = 2026-08-05T08:44:00+08:00
weight = 27
type = "docs"
description = "用包、crate 与模块组织不断增长的 Rust 项目"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 包、Crate 与模块 {#packages-crates-and-modules}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html](https://doc.rust-lang.org/stable/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html)


　　编写大型程序时，代码组织会变得越来越重要。把相关功能归到一起，并把职责不同的代码分开，你就能更清楚：要实现某个功能该去哪里找代码，要改某个行为又该动哪里。

　　迄今为止，我们写的程序都还只是一个文件里的一个模块。随着项目变大，你应该把代码拆成多个模块，再拆到多个文件里。一个包（package）可以包含多个二进制 crate，以及可选的一个库 crate。包继续变大时，还可以把一部分抽成独立的 crate，作为外部依赖。本章会介绍这些做法。对于由一组协同演进的包组成的超大项目，Cargo 还提供了工作空间（workspace），我们会在第 14 章的[「Cargo 工作空间」][workspaces]中讲解。

　　我们也会讨论如何封装实现细节，从而在更高层次复用代码：一旦你实现了某个操作，其他代码只需通过公共接口调用，而不必了解内部怎么工作。你写代码的方式，决定了哪些部分对外公开、可供其他代码使用，哪些部分是你保留修改权的私有实现细节。这也是一种减少你需要同时记在脑子里的细节数量的方式。

　　与此相关的概念是作用域（scope）：代码所处的嵌套上下文里，有一组被定义为「在作用域内」的名字。在阅读、编写和编译代码时，程序员和编译器都需要知道：某个位置上的某个名字究竟指的是变量、函数、结构体、枚举、模块、常量还是其他项，以及该项的含义是什么。你可以创建作用域，并改变哪些名字在作用域内或外。同一作用域里不能有两个同名项；也有工具可以用来解决命名冲突。

　　Rust 提供了许多特性来管理代码组织，包括哪些细节对外暴露、哪些细节私有，以及程序中每个作用域里有哪些名字。这些特性有时被统称为*模块系统*（module system），其中包括：

* **包（Packages）**：Cargo 提供的特性，用于构建、测试和共享 crate
* **Crate**：由模块组成的树，最终生成库或可执行文件
* **模块与 `use`**：用来控制路径的组织、作用域与私有性
* **路径（Paths）**：为结构体、函数或模块等项命名的方式

　　本章会介绍这些特性、它们如何协作，以及如何用它们管理作用域。读完之后，你应该能扎实掌握模块系统，并像老手一样自如地运用作用域！

[workspaces]: /trpl/more-about-cargo/03-cargo-workspaces/
