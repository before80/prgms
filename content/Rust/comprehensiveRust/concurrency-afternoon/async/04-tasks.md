+++
title = "2.5 任务"
date = 2026-08-11T11:30:00+08:00
weight = 373
type = "docs"
description = "04-任务 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/async/tasks.html](https://google.github.io/comprehensive-rust/concurrency/async/tasks.html)

# 2.5 任务

Rust 有一个任务系统，是一种轻量级线程形式。

一个任务有一个顶层 future，由 executor 轮询以推进。该 future 可能有一个或多个嵌套 future，由其 `poll` 方法轮询，大致对应调用栈。任务内的并发可以通过轮询多个子 future 实现，例如让定时器与 I/O 操作竞赛。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use tokio::io::{self, AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpListener;

#[tokio::main]
async fn main() -> io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:0").await?;
    println!("listening on port {}", listener.local_addr()?.port());

    loop {
        let (mut socket, addr) = listener.accept().await?;

        println!("connection from {addr:?}");

        tokio::spawn(async move {
            socket.write_all(b"Who are you?\n").await.expect("socket error");

            let mut buf = vec![0; 1024];
            let name_size = socket.read(&mut buf).await.expect("socket error");
            let name = std::str::from_utf8(&buf[..name_size]).unwrap().trim();
            let reply = format!("Thanks for dialing in, {name}!\n");
            socket.write_all(reply.as_bytes()).await.expect("socket error");
        });
    }
}
```

> 把本示例复制到准备好的 `src/main.rs` 并从那里运行。
>
> 试用 [nc](https://www.unix.com/man-page/linux/1/nc/) 或
> [telnet](https://www.unix.com/man-page/linux/1/telnet/) 等 TCP 连接工具连接它。
>
> - 请学员想象：有几个已连接客户端时，示例服务器的状态是什么。存在哪些任务？它们的 Future 是什么？
>
> - 这是我们第一次看到 `async` 块。它类似闭包，但不接受参数。其返回值是 Future，与 `async fn` 类似。
>
> - 把 async 块重构为函数，并用 `?` 改进错误处理。

