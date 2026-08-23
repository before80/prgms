+++
title = "2.2-索引"
date = 2026-08-22T19:00:00+08:00
weight = 4
type = "docs"
description = "索引"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# 索引 {#index}


> 原文链接: [https://rust-lang.github.io/async-book/navigation/index.html](https://rust-lang.github.io/async-book/navigation/index.html)


- Async/`async`
  - [块](../../part-guide/06-more-async-await-topics/#async-blocks)
  - [闭包](../../part-guide/06-more-async-await-topics/#async-closures)
  - [函数](../../part-guide/05-async-and-await/#async-functions)
  - [traits](../../part-guide/06-more-async-await-topics/#async-traits)
  - [对比线程](../../part-guide/04-concurrent-programming/#async-programming)
- [`await`](../../part-guide/05-async-and-await/#await)



- [阻塞](../../part-guide/06-more-async-await-topics/#blocking-and-cancellation)
  - [IO](../../part-guide/06-more-async-await-topics/#blocking-io)
  - [CPU 密集型任务](../../part-guide/07-io-and-issues-with-blocking/#other-blocking-operations)



- [取消](../../part-guide/06-more-async-await-topics/#cancellation)
  - [`CancellationToken`](../../part-guide/06-more-async-await-topics/#cancellation)
  - [在 `select` 中](../../part-guide/08-composing-futures-concurrently/#race-select)
- [并发](../../part-guide/04-concurrent-programming/)
  - [对比并行](../../part-guide/04-concurrent-programming/#concurrency-and-parallelism)
  - [原语（`join`、`select` 等）](../../part-guide/08-composing-futures-concurrently/)
- [协作式调度](../../part-guide/07-io-and-issues-with-blocking/#yielding)



- [执行器](../../part-guide/05-async-and-await/#the-runtime)



- [Future](../../part-guide/05-async-and-await/#futures-and-tasks)
  - `Future` trait



- [IO](../../part-guide/07-io-and-issues-with-blocking/)
  - [阻塞](../../part-guide/06-more-async-await-topics/#blocking-io)



- [`join`](../../part-guide/08-composing-futures-concurrently/#join)
- [加入任务](../../part-guide/05-async-and-await/#joining-tasks)
- [`JoinHandle`](../../part-guide/05-async-and-await/#joinhandle)
  - [`abort`](../../part-guide/06-more-async-await-topics/#cancellation)



- [多个运行时](../../part-guide/07-io-and-issues-with-blocking/#other-blocking-operations)
- 多任务
  - [协作式](../../part-guide/04-concurrent-programming/#async-programming)、[让出](../../part-guide/07-io-and-issues-with-blocking/#yielding)
  - [抢占式](../../part-guide/04-concurrent-programming/#processes-and-threads)



- [并行](../../part-guide/04-concurrent-programming/#concurrency-and-parallelism)
  - [对比并发](../../part-guide/04-concurrent-programming/#concurrency-and-parallelism)
- [固定、Pin](../../part-reference/17-pinning/)


- [`race`](../../part-guide/08-composing-futures-concurrently/#race-select)
- [反应器](../../part-guide/05-async-and-await/#the-runtime)
- [运行时](../../part-guide/05-async-and-await/#the-runtime)



- [调度器](../../part-guide/05-async-and-await/#the-runtime)
- [`select`](../../part-guide/08-composing-futures-concurrently/#race-select)
- [spawn 任务](../../part-guide/05-async-and-await/#spawning-tasks)



- [任务](../../part-guide/05-async-and-await/#futures-and-tasks)
  - [spawn](../../part-guide/05-async-and-await/#spawning-tasks)
- 测试
  - [单元测试](../../part-guide/06-more-async-await-topics/#unit-tests)
- [线程](../../part-guide/04-concurrent-programming/#processes-and-threads)
- [Tokio](../../part-guide/05-async-and-await/#the-runtime)
- Traits
  - [async](../../part-guide/06-more-async-await-topics/#async-traits)
  - `Future`
- [`try_join`](../../part-guide/08-composing-futures-concurrently/#join)



- [`Unpin`](../../part-reference/17-pinning/)



- [等待](../../part-guide/07-io-and-issues-with-blocking/#other-blocking-operations)



- [让出](../../part-guide/07-io-and-issues-with-blocking/#yielding)
- [`yield_now`](../../part-guide/07-io-and-issues-with-blocking/#yielding)
