+++
title = "3.1 异步通道"
date = 2026-08-11T11:30:00+08:00
weight = 375
type = "docs"
description = "01-异步通道 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/async-control-flow/channels.html](https://google.github.io/comprehensive-rust/concurrency/async-control-flow/channels.html)

# 3.1 异步通道

多个 crate 支持异步通道。例如 `tokio`：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use tokio::sync::mpsc;

async fn ping_handler(mut input: mpsc::Receiver<()>) {
    let mut count: usize = 0;

    while let Some(_) = input.recv().await {
        count += 1;
        println!("Received {count} pings so far.");
    }

    println!("ping_handler complete");
}

#[tokio::main]
async fn main() {
    let (sender, receiver) = mpsc::channel(32);
    let ping_handler_task = tokio::spawn(ping_handler(receiver));
    for i in 0..10 {
        sender.send(()).await.expect("Failed to send ping.");
        println!("Sent {} pings so far.", i + 1);
    }

    drop(sender);
    ping_handler_task.await.expect("Something went wrong in ping handler task.");
}
```

> - 把通道容量改成 `3`，观察对执行的影响。
>
> - 总体而言，接口与[上午课程](../channels.md)中的 `sync` 通道类似。
>
> - 试着去掉 `std::mem::drop` 调用。会发生什么？为什么？
>
> - [Flume](https://docs.rs/flume/latest/flume/) crate 的通道同时实现了 `sync` 与 `async` 的 `send` 与 `recv`。对于既有 IO 又有繁重 CPU 处理的复杂应用，这会很方便。
>
> - 使用 `async` 通道更可取之处在于：可以把它们与其他 `future` 组合，构建复杂控制流。

