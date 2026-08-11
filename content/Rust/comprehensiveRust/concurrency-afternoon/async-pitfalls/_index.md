+++
title = "4 陷阱"
date = 2026-08-11T11:30:00+08:00
weight = 378
type = "docs"
description = "陷阱 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/async-pitfalls.html](https://google.github.io/comprehensive-rust/concurrency/async-pitfalls.html)

# 4 陷阱

Async / await 为并发异步编程提供了方便且高效的抽象。不过，Rust 的 async/await 模型也有其陷阱与易踩坑点。本章举例说明其中一些。

本小节约需 55 分钟。内容包括：

| 内容 | 时长 |
| --- | --- |
| 阻塞执行器 | 10 分钟 |
| `Pin` | 20 分钟 |
| 异步 Trait | 5 分钟 |
| 取消 | 20 分钟 |

