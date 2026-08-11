+++
title = "4.2 `Pin`"
date = 2026-08-11T11:30:00+08:00
weight = 380
type = "docs"
description = "02-`Pin` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/async-pitfalls/pin.html](https://google.github.io/comprehensive-rust/concurrency/async-pitfalls/pin.html)

# 4.2 `Pin`

回想一下：async 函数或块会创建一个实现 `Future` 并包含所有局部变量的类型。其中一些变量可能持有指向其他局部变量的引用（指针）。为确保这些引用保持有效，该 future 绝不能被移动到不同的内存位置。

为防止 future 类型在内存中移动，只能通过固定指针（pinned pointer）对其进行轮询。`Pin` 是对引用的包装，禁止所有会把它所指向的实例移动到不同内存位置的操作。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use tokio::sync::{mpsc, oneshot};
use tokio::task::spawn;
use tokio::time::{Duration, sleep};

// 一个工作项。本例中只是休眠给定时间，并在 `respond_on` 通道上回复消息。
#[derive(Debug)]
struct Work {
    input: u32,
    respond_on: oneshot::Sender<u32>,
}

// 监听队列上的工作并执行它的 worker。
async fn worker(mut work_queue: mpsc::Receiver<Work>) {
    let mut iterations = 0;
    loop {
        tokio::select! {
            Some(work) = work_queue.recv() => {
                sleep(Duration::from_millis(10)).await; // 假装在工作。
                work.respond_on
                    .send(work.input * 1000)
                    .expect("failed to send response");
                iterations += 1;
            }
            // TODO: 每 100ms 报告迭代次数
        }
    }
}

// 请求工作并等待其完成的请求者。
async fn do_work(work_queue: &mpsc::Sender<Work>, input: u32) -> u32 {
    let (tx, rx) = oneshot::channel();
    work_queue
        .send(Work { input, respond_on: tx })
        .await
        .expect("failed to send on work queue");
    rx.await.expect("failed waiting for response")
}

#[tokio::main]
async fn main() {
    let (tx, rx) = mpsc::channel(10);
    spawn(worker(rx));
    for i in 0..100 {
        let resp = do_work(&tx, i).await;
        println!("work result for iteration {i}: {resp}");
    }
}
```

> - 你可能认出这是 actor 模式的例子。Actor 通常在循环中调用 `select!`。
>
> - 这是对前几课内容的综合，请慢慢消化。
>
>   - 天真地在 `select!` 中加入 `_ = sleep(Duration::from_millis(100)) => { println!(..) }`。这永远不会执行。为什么？
>
>   - 相反，在 `loop` 外加入包含该 future 的 `timeout_fut`：
>
>     ```rust
>     // Copyright 2024 Google LLC
>     // SPDX-License-Identifier: Apache-2.0
>     #
>     let timeout_fut = sleep(Duration::from_millis(100));
>     loop {
>         select! {
>             ..,
>             _ = timeout_fut => { println!(..); },
>         }
>     }
>     ```
>   - 这样仍不行。跟随编译器错误，在 `select!` 中给 `timeout_fut` 加上 `&mut` 以绕过移动，然后使用 `Box::pin`：
>
>     ```rust
>     // Copyright 2024 Google LLC
>     // SPDX-License-Identifier: Apache-2.0
>     #
>     let mut timeout_fut = Box::pin(sleep(Duration::from_millis(100)));
>     loop {
>         select! {
>             ..,
>             _ = &mut timeout_fut => { println!(..); },
>         }
>     }
>     ```
>
>   - 这能编译，但超时一旦到期，之后每次迭代都是 `Poll::Ready`（fused future 对此有帮助）。更新为每次到期时重置 `timeout_fut`：
>     ```rust
>     // Copyright 2024 Google LLC
>     // SPDX-License-Identifier: Apache-2.0
>     #
>     let mut timeout_fut = Box::pin(sleep(Duration::from_millis(100)));
>     loop {
>         select! {
>             _ = &mut timeout_fut => {
>                 println!(..);
>                 timeout_fut = Box::pin(sleep(Duration::from_millis(100)));
>             },
>         }
>     }
>     ```
>
> - `Box` 在堆上分配。在某些情况下，`std::pin::pin!`（最近才稳定，旧代码常用 `tokio::pin!`）也是选项，但对会重新赋值的 future 很难用。
>
> - 另一替代方案是完全不用 `pin`，而是再派生一个任务，每 100ms 向 `oneshot` 通道发送一次。
>
> - 包含指向自身指针的数据称为自引用（self-referential）。通常，Rust 借用检查器会阻止自引用数据被移动，因为引用不能比它们指向的数据活得更久。然而，async 块与函数的代码转换未经借用检查器验证。
>
> - `Pin` 是对引用的包装。不能通过固定指针把对象从其所在位置移走。但仍可通过未固定指针移动它。
>
> - `Future` trait 的 `poll` 方法使用 `Pin<&mut Self>` 而不是 `&mut Self` 来引用实例。这就是为什么只能在固定指针上调用它。

