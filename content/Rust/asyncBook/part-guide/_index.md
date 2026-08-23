+++
title = "3-简介"
date = 2026-08-22T19:00:00+08:00
weight = 18
type = "docs"
description = "简介"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 简介 {#introduction}


> 原文链接: [https://rust-lang.github.io/async-book/part-guide/intro.html](https://rust-lang.github.io/async-book/part-guide/intro.html)


本书的这一部分是 async Rust 的教程式指南。面向 Rust 异步编程的新手。无论你是否在其他语言中做过异步编程，都应该会有帮助。如果你有经验，可以跳过或略读第一节。你可能还想尽早阅读这篇[与其他语言 async 的对比]()。

## 核心概念

我们将首先讨论不同的[并发编程](04-concurrent-programming/)模型，使用进程、线程或异步任务。第一章将涵盖 Rust async 模型的核心部分，然后我们在[第二章](../async-await/)深入 async 编程的细节，介绍 async 和 await 编程范式。我们在[后续章节](06-more-async-await-topics/)中涵盖更多 async 编程概念。

async 编程的主要动机之一是更高性能的 IO，我们在[下一章](07-io-and-issues-with-blocking/)中涵盖。我们还在同一章中详细讨论*阻塞*。阻塞是 async 编程中的主要隐患，线程被某个操作（通常是 IO）同步等待而阻塞，无法继续推进。

async 编程的另一个动机是它促进了[并发代码的抽象与组合](08-composing-futures-concurrently/)的新模型。涵盖该内容后，我们继续讨论并发任务之间的[同步](09-channels-locking-and-synchronization/)。

有一章关于 [async 编程工具](10-tools-for-async-programming/)。

最后几章涵盖一些更专业的主题，从[异步析构与清理](11-destruction-and-clean-up/)开始（这是常见需求，但由于目前没有好的内置解决方案，属于较为专业的话题）。

指南中的接下来两章深入讲解 [future](12-futures/) 和[运行时](13-runtimes/)，这是 async 编程的两个基本构建块。

最后，我们涵盖[定时器与信号处理](14-timers-and-signal-handling/)和[异步迭代器](../streams/)（即流）。后者是我们处理异步事件序列的方式（对比用 future 或异步函数表示的单个异步事件）。这是语言正在积极开发的领域，可能有些粗糙。
