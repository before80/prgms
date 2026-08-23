+++
title = "14-定时器与信号处理"
date = 2026-08-22T19:00:00+08:00
weight = 16
type = "docs"
description = "定时器与信号处理"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 定时器与信号处理 {#timers-and-signal-handling}


> 原文链接: [https://rust-lang.github.io/async-book/part-guide/timers-signals.html](https://rust-lang.github.io/async-book/part-guide/timers-signals.html)


## 时间与定时器

- 运行时集成，不要使用 thread::sleep 等
- std Instant 和 Duration
- sleep
- interval
- timeout
  - 特殊 future vs select/race

## 信号处理

- 什么是信号处理，为什么它是 async 问题？
- 非常依赖操作系统
- 参见 Tokio 文档
