+++
title = "第8章 并发"
date = 2026-08-06T17:08:00+08:00
weight = 38
type = "docs"
description = "并发与并行的底层问题"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 并发


> 原文链接: [https://doc.rust-lang.org/nomicon/concurrency.html](https://doc.rust-lang.org/nomicon/concurrency.html)


　　作为语言，Rust *并不*对如何做并发或并行持有强立场。标准库暴露 OS 线程和阻塞式系统调用，因为人人都有这些，且足够统一，可以在相对无争议的方式下提供抽象。消息传递、绿色线程和 async API 都足够多样，任何覆盖它们的抽象往往涉及我们在 1.0 不愿承诺的权衡。

　　然而 Rust 建模并发的方式，使得设计自己的并发范式作为库相对容易，且他人的代码能与你的方案无缝协作。只需在合适处要求正确的 lifetime 以及 `Send` 和 `Sync`，你就可以放手开跑——或者更准确地说，放手开跑且……没有……竞态。
