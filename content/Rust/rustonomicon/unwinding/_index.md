+++
title = "第7章 展开（Unwinding）"
date = 2026-08-06T17:08:00+08:00
weight = 35
type = "docs"
description = "panic 展开与异常安全"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 展开（Unwinding）


> 原文链接: [https://doc.rust-lang.org/nomicon/unwinding.html](https://doc.rust-lang.org/nomicon/unwinding.html)


　　Rust 采用*分层*的错误处理方案：

* 若某值可能合理地不存在，使用 `Option`。
* 若出错且可以合理地处理，使用 `Result`。
* 若出错且无法合理地处理，线程 panic。
* 若发生灾难性错误，程序 abort。

　　在绝大多数情况下，`Option` 和 `Result` 都更受青睐，尤其是因为调用方可以自行决定是否在 API 边界将其提升为 panic 或 abort。
　　panic 会使线程停止正常执行并展开其栈，就好像每个函数都瞬间返回一样，同时调用析构函数。

　　自 1.0 起，Rust 对 panic 的态度有些分裂。在很久以前，Rust 更像 Erlang：像 Erlang 一样，Rust 有轻量级任务（task），任务在陷入无法维持的状态时会用 panic 自杀。
　　与 Java 或 C++ 中的异常不同，panic 在任意时刻都无法被捕获；只有任务的所有者能捕获 panic，此时必须处理，否则*该*任务本身也会 panic。

　　展开对这一模型很重要，因为如果任务的析构函数不被调用，内存和其他系统资源就会泄漏。由于任务在正常执行中预期会死亡，这会让 Rust 非常不适合长期运行的系统！

　　随着我们今天所知的 Rust 逐渐形成，这种编程风格在追求更少抽象的过程中逐渐失宠。轻量级任务为重量级 OS 线程让路。即便如此，在 1.0 的稳定 Rust 中，panic 仍只能被父线程捕获。这意味着捕获 panic 需要启动一整个 OS 线程！这不幸与 Rust 零成本抽象的理念相冲突。

　　有一个名为 [`catch_unwind`] 的 API，可以在不创建线程的情况下捕获 panic。不过我们仍建议你谨慎使用。尤其 Rust 当前的展开实现针对「不展开」的情况做了大量优化。若程序不展开，为*准备好*展开而付出的运行时成本应为零。因此，实际展开会比 Java 等语言更昂贵。
　　不要让你的程序在正常流程下依赖展开。理想情况下，你只应因编程错误或*极端*问题而 panic。

　　Rust 的展开策略并未规定与其他语言的展开在根本上兼容。因此，从其他语言展开进入 Rust，或从 Rust 展开进入其他语言，都是未定义行为（Undefined Behavior）。
　　你*必须*在 FFI 边界捕获所有 panic！此后如何处理由你决定，但*必须*做点什么。若未做到，最好情况下程序会崩溃；最坏情况下程序*不会*崩溃，却会在完全混乱的状态下继续运行。

[`catch_unwind`]: https://doc.rust-lang.org/std/panic/fn.catch_unwind.html
