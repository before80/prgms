+++
title = "2.1-按主题浏览"
date = 2026-08-22T19:00:00+08:00
weight = 3
type = "docs"
description = "按主题浏览"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 按主题浏览 {#by-topic}


> 原文链接: [https://rust-lang.github.io/async-book/navigation/topics.html](https://rust-lang.github.io/async-book/navigation/topics.html)


## 并发与并行

- [简介](../../part-guide/04-concurrent-programming/#concurrency-and-parallelism)
- [使用 `spawn` 并行运行异步任务](../../part-guide/05-async-and-await/#spawning-tasks)
- [使用 `join` 和 `select` 并发运行 future](../../part-guide/08-composing-futures-concurrently/)
- [混合同步与异步并发](../../part-guide/07-io-and-issues-with-blocking/#other-blocking-operations)


## 正确性与安全性

- 取消
  - [简介](../../part-guide/06-more-async-await-topics/#cancellation)
  - [在 `select` 和 `try_join` 中](../../part-guide/08-composing-futures-concurrently/)


## 性能

- 阻塞
  - [简介](../../part-guide/06-more-async-await-topics/#blocking-and-cancellation)
  - [阻塞与非阻塞 IO](../../part-guide/07-io-and-issues-with-blocking/)
  - [CPU 密集型代码](../../part-guide/07-io-and-issues-with-blocking/#other-blocking-operations)


## 测试

- [单元测试语法](../../part-guide/06-more-async-await-topics/#unit-tests)
