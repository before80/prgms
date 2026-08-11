+++
title = "2.4 运行时"
date = 2026-08-11T11:30:00+08:00
weight = 371
type = "docs"
description = "运行时 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/async/runtimes.html](https://google.github.io/comprehensive-rust/concurrency/async/runtimes.html)

# 2.4 运行时

*运行时*（runtime）提供异步执行操作的支持（*reactor*），并负责执行 futures（*executor*）。Rust 没有「内置」运行时，但有多种可选方案：

- [Tokio](https://tokio.rs/)：性能好，生态系统完善，例如用于 HTTP 的 [Hyper](https://hyper.rs/)，或用于 gRPC 的 [Tonic](https://github.com/hyperium/tonic)。
- [smol](https://docs.rs/smol/latest/smol/)：简单轻量

一些更大的应用有自己的运行时。例如
[Fuchsia](https://fuchsia.googlesource.com/fuchsia/+/refs/heads/main/src/lib/fuchsia-async/src/lib.rs)
已有一个。

> - 注意：所列运行时中，只有 Tokio 在 Rust playground 中受支持。playground 也不允许任何 I/O，因此多数有趣的异步内容无法在 playground 中运行。
>
> - Future 是「惰性」的：除非有 executor 轮询它们，否则它们什么也不做（甚至不会启动 I/O 操作）。这与 JS Promise 不同——例如即使从未使用，Promise 也会运行到完成。

