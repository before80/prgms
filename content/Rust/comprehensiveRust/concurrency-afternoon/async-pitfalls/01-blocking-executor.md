+++
title = "4.1 阻塞执行器"
date = 2026-08-11T11:30:00+08:00
weight = 379
type = "docs"
description = "01-阻塞执行器 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/async-pitfalls/blocking-executor.html](https://google.github.io/comprehensive-rust/concurrency/async-pitfalls/blocking-executor.html)

# 4.1 阻塞执行器

多数异步运行时只允许 I/O 任务并发运行。这意味着 CPU 阻塞任务会阻塞执行器，并阻止其他任务执行。简便的变通办法是尽可能使用异步等价方法。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use futures::future::join_all;
use std::time::Instant;

async fn sleep_ms(start: &Instant, id: u64, duration_ms: u64) {
    std::thread::sleep(std::time::Duration::from_millis(duration_ms));
    println!(
        "future {id} slept for {duration_ms}ms, finished after {}ms",
        start.elapsed().as_millis()
    );
}

#[tokio::main(flavor = "current_thread")]
async fn main() {
    let start = Instant::now();
    let sleep_futures = (1..=10).map(|t| sleep_ms(&start, t, t * 10));
    join_all(sleep_futures).await;
}
```

> - 运行代码，会看到休眠是连续发生的，而不是并发的。
>
> - `"current_thread"` flavor 把所有任务放在单个线程上。这使效果更明显，但在多线程 flavor 中该缺陷仍然存在。
>
> - 把 `std::thread::sleep` 换成 `tokio::time::sleep` 并 await 其结果。
>
> - 另一种修复是 `tokio::task::spawn_blocking`：它派生真正的线程，并把其句柄变成 future，而不会阻塞执行器。
>
> - 不应把任务想成操作系统线程。它们不是 1 对 1 映射的；执行器会允许多个任务在单个 OS 线程上运行。通过 FFI 与其他库交互时这尤其成问题，因为那些库可能依赖线程局部存储，或映射到特定 OS 线程（例如 CUDA）。在这种情况下优先使用 `tokio::task::spawn_blocking`。
>
> - 谨慎使用同步互斥锁。在 `.await` 期间持有互斥锁可能导致另一任务阻塞，而该任务可能运行在同一线程上。

