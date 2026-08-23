+++
title = "25-异步生态"
date = 2026-08-22T19:00:00+08:00
weight = 43
type = "docs"
description = "异步生态"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 异步生态 {#the-async-ecosystem}


> 原文链接: [https://rust-lang.github.io/async-book/08_ecosystem/00_chapter.html](https://rust-lang.github.io/async-book/08_ecosystem/00_chapter.html)


Rust 目前仅提供编写异步代码的基本要素。重要的是，执行器、任务、反应器、组合子以及底层 IO future 和 trait 尚未纳入标准库。与此同时，社区提供的异步生态填补了这些空白。

Async Foundations 团队有兴趣扩展异步书中的示例以涵盖多个运行时。若你有兴趣为此项目做贡献，请在 [Zulip](https://rust-lang.zulipchat.com/#narrow/stream/201246-wg-async-foundations.2Fbook) 上联系我们。

## 异步运行时

异步运行时是用于执行异步应用的库。运行时通常将*反应器*与一个或多个*执行器*捆绑在一起。反应器为外部事件（如异步 IO、进程间通信和定时器）提供订阅机制。在异步运行时中，订阅者通常是表示底层 IO 操作的 future。执行器处理任务的调度与执行。它们跟踪运行中和挂起的任务，将 future poll 至完成，并在任务可以推进时唤醒任务。「执行器」一词常与「运行时」互换使用。此处我们用「生态」描述与兼容 trait 和功能捆绑的运行时。

## 社区提供的异步 Crate

### Futures Crate

[`futures` crate](https://docs.rs/futures/) 包含编写异步代码有用的 trait 和函数。这包括 `Stream`、`Sink`、`AsyncRead` 和 `AsyncWrite` trait，以及组合子等工具。这些工具和 trait 最终可能成为标准库的一部分。

`futures` 有自己的执行器，但没有自己的反应器，因此不支持异步 IO 或定时器 future 的执行。因此，它不被视为完整运行时。常见选择是将 `futures` 的工具与另一 crate 的执行器配合使用。

### 流行的异步运行时

标准库中没有异步运行时，也没有官方推荐的。以下 crate 提供流行的运行时。

- [Tokio](https://docs.rs/tokio/)：流行的异步生态，带有 HTTP、gRPC 和追踪框架。
- [async-std](https://docs.rs/async-std/)：提供标准库组件异步对应物的 crate。
- [smol](https://docs.rs/smol/)：小型、简化的异步运行时。提供可用于包装 `UnixStream` 或 `TcpListener` 等结构的 `Async` trait。
- [fuchsia-async](https://fuchsia.googlesource.com/fuchsia/+/master/src/lib/fuchsia-async/)：用于 Fuchsia OS 的执行器。

## 确定生态兼容性

并非所有异步应用、框架和库彼此兼容，或与每个 OS 或平台兼容。大多数异步代码可与任何生态配合使用，但某些框架和库要求使用特定生态。生态约束并不总是有文档说明，但有几条经验法则可判断库、trait 或函数是否依赖特定生态。

任何与异步 IO、定时器、进程间通信或任务交互的异步代码，通常依赖特定异步执行器或反应器。所有其他异步代码，如异步表达式、组合子、同步类型和流，通常是生态无关的，前提是任何嵌套的 future 也是生态无关的。开始项目前，建议调研相关异步框架和库，确保与所选运行时以及彼此兼容。

值得注意的是，`Tokio` 使用 `mio` 反应器并定义自己的异步 IO trait 版本，包括 `AsyncRead` 和 `AsyncWrite`。就其本身而言，它与依赖 [`async-executor` crate](https://docs.rs/async-executor) 以及 `futures` 中定义的 `AsyncRead` 和 `AsyncWrite` trait 的 `async-std` 和 `smol` 不兼容。

冲突的运行时要求有时可通过兼容层解决，允许你在一个运行时内调用为另一运行时编写的代码。例如，[`async_compat` crate](https://docs.rs/async_compat) 提供 `Tokio` 与其他运行时之间的兼容层。

暴露异步 API 的库不应依赖特定执行器或反应器，除非需要生成任务或定义自己的异步 IO 或定时器 future。理想情况下，只有二进制文件应负责调度和运行任务。

## 单线程与多线程执行器

异步执行器可以是单线程或多线程的。例如，`async-executor` crate 既有单线程 `LocalExecutor`，也有多线程 `Executor`。

多线程执行器可同时推进多个任务。对任务众多的工作负载，它可以大幅加速执行，但任务间同步数据通常更昂贵。在选择单线程还是多线程运行时时，建议为你的应用测量性能。

任务可以在创建它们的线程上运行，也可以在单独线程上运行。异步运行时通常提供在单独线程上生成任务的功能。即使任务在单独线程上执行，它们仍应是非阻塞的。要在多线程执行器上调度任务，它们还必须是 `Send` 的。某些运行时提供生成非 `Send` 任务的函数，确保每个任务在生成它的线程上执行。它们还可能提供在专用线程上生成阻塞任务的函数，这对从其他库运行阻塞同步代码很有用。
