+++
title = "1-简介"
date = 2026-08-22T19:00:00+08:00
weight = 2
type = "docs"
description = "简介"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 简介 {#introduction}


> 原文链接: [https://rust-lang.github.io/async-book/intro.html](https://rust-lang.github.io/async-book/intro.html)


注意：本指南目前正在进行重写，因为长时间没有大量更新。内容仍在编写中，许多部分尚缺，现有内容也有些粗糙。


本书是 Rust 异步编程指南。它旨在帮助你迈出第一步，并探索更高级的主题。我们不假定你有任何异步编程经验（无论是在 Rust 还是其他语言中），但假定你已经熟悉 Rust。如果你想学习 Rust，可以从 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/) 开始。

本书有两个主要部分：[第一部分](../part-guide/) 是初学者指南，设计为按顺序阅读，带你从零基础到中级水平。第二部分是关于更高级主题的独立章节集合。完成第一部分后，或者如果你已有一些 async Rust 经验，第二部分会很有用。

你可以通过多种方式浏览本书：

* 你可以从头到尾按顺序阅读。对于 async Rust 新手，至少对于本书的[第一部分](../part-guide/)，这是推荐的路径。
* 网页左侧有目录摘要。
* 如果你想了解某个宽泛主题的信息，可以从主题索引开始。
* 如果你想找到关于某个特定主题的所有讨论，可以从详细索引开始。
* 你可以看看常见问题解答中是否已有你的问题的答案。


## 什么是异步编程，为什么要用它？

在并发编程中，程序同时做多件事（或至少看起来是这样）。使用线程编程是并发编程的一种形式。线程内的代码以顺序风格编写，操作系统并发地执行线程。在异步编程中，并发完全发生在你的程序内部（操作系统不参与）。异步运行时（在 Rust 中只是另一个 crate）与程序员通过 `await` 关键字显式让出控制权来协同管理异步任务。

由于操作系统不参与，异步世界中的*上下文切换*非常快。此外，异步任务的内存开销远低于操作系统线程。这使得异步编程非常适合需要处理大量并发任务、且这些任务花费大量时间等待（例如等待客户端响应或 IO）的系统。它也适合内存非常有限、且没有提供线程的操作系统的微控制器。

异步编程还为程序员提供了对任务执行方式的细粒度控制（并行度和并发度、控制流、调度等）。这意味着异步编程在许多用途上既富有表现力又易于使用。特别是，Rust 中的异步编程具有强大的取消概念，并支持多种不同风格的并发（通过 `spawn` 及其变体、`join`、`select`、`for_each_concurrent` 等构造来表达）。这些允许实现可组合、可复用的概念，如超时、暂停和节流。


## Hello, world!

为了让你感受一下 async Rust 的样子，这里有一个 "hello, world" 示例。它没有并发，也没有真正利用异步的优势。但它定义并使用了异步函数，并打印了 "hello, world!"：

```rust,edition2021
// 定义一个异步函数。
async fn say_hello() {
    println!("hello, world!");
}

#[tokio::main] // 样板代码，让我们可以写 `async fn main`，稍后解释。
async fn main() {
    // 调用异步函数并 await 其结果。
    say_hello().await;
}
```

我们稍后会详细解释一切。现在，请注意我们如何使用 `async fn` 定义异步函数，以及如何使用 `.await` 调用它——Rust 中的异步函数除非被 `await`，否则不会执行任何操作[^blocking]。

与本书中的所有示例一样，如果你想查看完整示例（包括 `Cargo.toml` 等），或在本地自己运行，可以在本书的 GitHub 仓库中找到：例如 [examples/hello-world](https://github.com/rust-lang/async-book/tree/master/examples/hello-world)。


## Async Rust 的发展

Rust 的异步特性已经开发了一段时间，但它还不是语言的"完成"部分。Async Rust（至少在稳定编译器和标准库中可用的部分）是可靠且高性能的。它在一些最苛刻的场景中被用于生产环境，包括大型科技公司。然而，仍有一些缺失的部分和粗糙之处（粗糙指的是易用性而非可靠性）。在 async Rust 的学习旅程中，你很可能会遇到一些这样的部分。对于大多数缺失的部分，都有变通方案，本书会涵盖这些内容。

目前，使用异步迭代器（也称为流）是大多数用户发现有些粗糙的地方。traits 中 async 的某些用法尚未得到良好支持。异步析构还没有好的解决方案。

Async Rust 正在积极开发中。如果你想关注开发进展，可以查看 Async Working Group 的[主页](https://rust-lang.github.io/wg-async/meetings.html)，其中包括他们的[路线图](https://rust-lang.github.io/wg-async/vision/roadmap.html)。或者你可以阅读 Rust 项目中的 async [项目目标](https://github.com/rust-lang/rust-project-goals/issues/105)。

Rust 是一个开源项目。如果你想为 async Rust 的开发做出贡献，可以从主 Rust 仓库的[贡献文档](https://github.com/rust-lang/rust/blob/master/CONTRIBUTING.md)开始。


[^blocking]: 这实际上是一个不好的示例，因为 `println` 是*阻塞 IO*，在异步函数中进行阻塞 IO 通常是一个坏主意。我们会在 [chapter TODO]() 中解释什么是阻塞 IO，并在 [chapter TODO]() 中解释为什么不应该在异步函数中进行阻塞 IO。
