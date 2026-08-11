+++
title = "2.4.1 Tokio"
date = 2026-08-11T11:30:00+08:00
weight = 372
type = "docs"
description = "01-Tokio — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/async/runtimes/tokio.html](https://google.github.io/comprehensive-rust/concurrency/async/runtimes/tokio.html)

# 2.4.1 Tokio

Tokio 提供：

- 用于执行异步代码的多线程运行时。
- 标准库的异步版本。
- 庞大的库生态系统。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use tokio::time;

async fn count_to(count: i32) {
    for i in 0..count {
        println!("Count in task: {i}!");
        time::sleep(time::Duration::from_millis(5)).await;
    }
}

#[tokio::main]
async fn main() {
    tokio::spawn(count_to(10));

    for i in 0..5 {
        println!("Main task: {i}");
        time::sleep(time::Duration::from_millis(5)).await;
    }
}
```

> - 借助 `tokio::main` 宏，我们现在可以把 `main` 做成 async。
>
> - `spawn` 函数会创建新的并发「任务」。
>
> - 注意：`spawn` 接受一个 `Future`，你不要对 `count_to` 调用 `.await`。
>
> **深入探索：**
>
> - 为何 `count_to` 数不到 10？这是异步取消的例子。`tokio::spawn` 返回一个句柄，可以 await 它以等待任务完成。
>
> - 试着用 `count_to(10).await` 而不是 spawn。
>
> - 试着 await `tokio::spawn` 返回的任务。

