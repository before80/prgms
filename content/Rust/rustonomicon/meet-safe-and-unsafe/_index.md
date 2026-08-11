+++
title = "第1章 认识 Safe 与 Unsafe"
date = 2026-08-06T17:08:00+08:00
weight = 2
type = "docs"
description = "Safe Rust 与 Unsafe Rust 的分界与协作"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 认识 Safe 与 Unsafe


> 原文链接: [https://doc.rust-lang.org/nomicon/meet-safe-and-unsafe.html](https://doc.rust-lang.org/nomicon/meet-safe-and-unsafe.html)


　　![safe and unsafe](img/safeandunsafe.svg)

　　若能不必操心底层实现细节，那该多好。
　　谁会真的在意空元组占多少空间呢？遗憾的是，有时这确实重要，我们不得不关心。开发者开始在意实现细节，最常见的原因是性能；但更重要的是，当直接与硬件、操作系统或其他语言打交道时，这些细节会变成正确性问题。

　　当实现细节在「安全」编程语言里开始重要时，程序员通常有三条路：

* 摆弄代码，诱使编译器/运行时做某种优化
* 采用更不合习惯或更笨拙的设计，以得到想要的实现
* 用允许你处理这些细节的语言重写实现

　　对最后一条路，程序员往往选 *C*。要与只提供 C 接口的系统对接，这常常是必要的。

　　不幸的是，C 用起来极不安全（有时也有充分理由），而在与另一种语言互操作时，这种不安全会被放大。必须小心确保 C 与另一语言对「发生了什么」有一致理解，且互不踩踏。

　　这与 Rust 有何关系？

　　嗯，与 C 不同，Rust 是一门安全编程语言。

　　但，与 C 一样，Rust 也是一门不安全编程语言。

　　更准确地说，Rust *同时包含* 安全与不安全两种编程语言。

　　Rust 可看作两种语言的组合：*Safe Rust* 与 *Unsafe Rust*。名字名副其实：Safe Rust 是安全的；Unsafe Rust 则不然。事实上，Unsafe Rust 让我们能做*非常*不安全的事——Rust 作者会恳请你别做，但我们会做。

　　Safe Rust 才是*真正的* Rust 编程语言。若你只写 Safe Rust，就永远不必操心类型安全或内存安全。你不会遇到悬垂指针、释放后使用，或任何其他未定义行为（Undefined Behavior，简称 UB）。

　　标准库也提供了足够工具，让你能用纯惯用的 Safe Rust 写出高性能应用与库。

　　但也许你要与另一种语言对话；也许在写标准库未暴露的底层抽象；也许在*编写*标准库（它完全用 Rust 写成）；也许要做类型系统不理解的事，只好*直接摆弄比特*。这时你需要 Unsafe Rust。

　　Unsafe Rust 与 Safe Rust 规则与语义相同，只是额外允许一些明确不安全（Definitely Not Safe）的操作（下一节会定义）。

　　这种分离的价值在于：我们获得像 C 这类不安全语言的益处——对实现细节的底层控制——又不必承受把它与完全不同的安全语言集成时的大多数问题。

　　仍有一些问题——尤其我们必须意识到类型系统所假设的性质，并在任何与 Unsafe Rust 交互的代码中审计它们。本书的目的就是教你这些假设以及如何管理它们。
