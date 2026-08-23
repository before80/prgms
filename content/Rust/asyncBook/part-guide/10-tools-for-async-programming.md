+++
title = "10-异步编程工具"
date = 2026-08-22T19:00:00+08:00
weight = 12
type = "docs"
description = "异步编程工具"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 异步编程工具 {#tools-for-async-programming}


> 原文链接: [https://rust-lang.github.io/async-book/part-guide/tools.html](https://rust-lang.github.io/async-book/part-guide/tools.html)


- 为什么需要专门的 async 工具
- 是否还有其他需要涵盖的工具
  - loom

## 监控

- [Tokio console](https://github.com/tokio-rs/console)

## 追踪与日志

- async 追踪的问题
- tracing crate（https://github.com/tokio-rs/tracing）

## 调试

- 理解 async 回溯（RUST_BACKTRACE 和在调试器中）
- 调试 async 代码的技术
- 使用 Tokio console 进行调试
- 调试器支持（WinDbg？）

## 性能分析

- async 如何干扰火焰图
- 如何分析 async IO
- 深入了解运行时
  - Tokio metrics
