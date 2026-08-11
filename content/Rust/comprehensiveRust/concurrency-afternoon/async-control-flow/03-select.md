+++
title = "3.3 Select"
date = 2026-08-11T11:30:00+08:00
weight = 377
type = "docs"
description = "03-Select — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/async-control-flow/select.html](https://google.github.io/comprehensive-rust/concurrency/async-control-flow/select.html)

# 3.3 Select

select 操作会等待一组 future 中的任意一个就绪，并对该 future 的结果作出响应。在 JavaScript 中类似 `Promise.race`。在 Python 中可对比
`asyncio.wait(task_set, return_when=asyncio.FIRST_COMPLETED)`。

与 match 语句类似，`select!` 的主体有若干分支，每个形如 `pattern = future => statement`。当某个 `future` 就绪时，其返回值由 `pattern` 解构，然后用得到的变量运行 `statement`。`statement` 的结果成为 `select!` 宏的结果。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use tokio::sync::mpsc;
use tokio::time::{Duration, sleep};

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel(32);
    let listener = tokio::spawn(async move {
        tokio::select! {
            Some(msg) = rx.recv() => println!("got: {msg}"),
            _ = sleep(Duration::from_millis(50)) => println!("timeout"),
        };
    });
    sleep(Duration::from_millis(10)).await;
    tx.send(String::from("Hello!")).await.expect("Failed to send greeting");

    listener.await.expect("Listener failed");
}
```

> - 这里的 `listener` async 块是常见形式：等待某个异步事件，或等待超时。把 `sleep` 改得更长以观察失败。为何在这种情况下 `send` 也会失败？
>
> - `select!` 也常在「actor」架构的循环中使用：任务在循环中对事件作出反应。这有一些陷阱，将在下一段讨论。

