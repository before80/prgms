+++
title = "3.1 发送端与接收端"
date = 2026-08-11T11:30:00+08:00
weight = 349
type = "docs"
description = "01-发送端与接收端 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/channels/senders-receivers.html](https://google.github.io/comprehensive-rust/concurrency/channels/senders-receivers.html)

# 3.1 发送端与接收端

Rust 通道有两部分：[`Sender<T>`] 与 [`Receiver<T>`]。两端通过通道相连，但你只能看到端点。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::sync::mpsc;

fn main() {
    let (tx, rx) = mpsc::channel();

    tx.send(10).unwrap();
    tx.send(20).unwrap();

    println!("Received: {:?}", rx.recv());
    println!("Received: {:?}", rx.recv());

    let tx2 = tx.clone();
    tx2.send(30).unwrap();
    println!("Received: {:?}", rx.recv());
}
```

> - [`mpsc`] 表示 Multi-Producer, Single-Consumer（多生产者、单消费者）。`Sender` 与 `SyncSender` 实现了 `Clone`（因此可以有多个生产者），但 `Receiver` 没有。
> - [`send()`] 与 [`recv()`] 返回 `Result`。若返回 `Err`，表示对端的 `Sender` 或 `Receiver` 已丢弃，通道已关闭。


[`Sender<T>`]: https://doc.rust-lang.org/std/sync/mpsc/struct.Sender.html
[`Receiver<T>`]: https://doc.rust-lang.org/std/sync/mpsc/struct.Receiver.html
[`send()`]: https://doc.rust-lang.org/std/sync/mpsc/struct.Sender.html#method.send
[`recv()`]: https://doc.rust-lang.org/std/sync/mpsc/struct.Receiver.html#method.recv
[`mpsc`]: https://doc.rust-lang.org/std/sync/mpsc/index.html
