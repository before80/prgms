+++
title = "1 欢迎"
date = 2026-08-11T11:30:00+08:00
weight = 366
type = "docs"
description = "01-欢迎 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/welcome-async.html](https://google.github.io/comprehensive-rust/concurrency/welcome-async.html)

# 1 欢迎

「异步」（async）是一种并发模型：通过执行每个任务直到即将阻塞，再切换到另一个可以继续推进的任务，从而并发执行多个任务。该模型能在有限数量的线程上运行更多任务，因为每个任务的开销通常很低，而且操作系统提供了高效识别可继续进行的 I/O 的原语。

Rust 的异步操作基于「futures」：表示将来可能完成的工作。Future 会被「轮询」（poll），直到它们表明已完成。

Future 由异步运行时（async runtime）轮询，有多种不同的运行时可供选择。

## 对比

- Python 的 `asyncio` 中有类似模型。不过其 `Future` 类型基于回调，而非轮询。异步 Python 程序需要一个「循环」，类似于 Rust 中的运行时。

- JavaScript 的 `Promise` 类似，同样基于回调。语言运行时实现了事件循环，因此 Promise 解析的多数细节被隐藏起来。

## 日程

含每次 10 分钟休息，本时段约需 3 小时 30 分钟。内容包括：

| 小节 | 时长 |
| --- | --- |
| 异步基础 | 40 分钟 |
| 通道与控制流 | 20 分钟 |
| 陷阱 | 55 分钟 |
| 练习 | 1 小时 10 分钟 |

