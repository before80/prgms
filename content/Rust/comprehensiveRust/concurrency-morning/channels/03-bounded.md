+++
title = "3.3 有界通道"
date = 2026-08-11T11:30:00+08:00
weight = 351
type = "docs"
description = "03-有界通道 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/channels/bounded.html](https://google.github.io/comprehensive-rust/concurrency/channels/bounded.html)

# 3.3 有界通道

使用有界（同步）通道时，[`send()`] 可能阻塞当前线程：

```rust
// Copyright 2022 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

fn main() {
    let (tx, rx) = mpsc::sync_channel(3);

    thread::spawn(move || {
        let thread_id = thread::current().id();
        for i in 0..10 {
            tx.send(format!("Message {i}")).unwrap();
            println!("{thread_id:?}: sent Message {i}");
        }
        println!("{thread_id:?}: done");
    });
    thread::sleep(Duration::from_millis(100));

    for msg in rx {
        println!("Main: got {msg}");
    }
}
```

> - 调用 `send()` 会阻塞当前线程，直到通道中有空间容纳新消息。若没有人从通道读取，线程可能无限阻塞。
> - 与无界通道一样，若通道已关闭，调用 `send()` 会以错误中止。
> - 容量为零的有界通道称为「会合通道」（rendezvous channel）。每次发送都会阻塞当前线程，直到另一线程调用 [`recv()`]。


[`send()`]: https://doc.rust-lang.org/std/sync/mpsc/struct.SyncSender.html#method.send
[`recv()`]: https://doc.rust-lang.org/std/sync/mpsc/struct.Receiver.html#method.recv
