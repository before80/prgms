+++
title = "3.2 无界通道"
date = 2026-08-11T11:30:00+08:00
weight = 350
type = "docs"
description = "02-无界通道 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/channels/unbounded.html](https://google.github.io/comprehensive-rust/concurrency/channels/unbounded.html)

# 3.2 无界通道

用 [`mpsc::channel()`] 可以得到无界、异步的通道：

```rust
// Copyright 2022 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

fn main() {
    let (tx, rx) = mpsc::channel();

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

[`mpsc::channel()`]: https://doc.rust-lang.org/std/sync/mpsc/fn.channel.html

> - 无界通道会按需分配空间来存放待处理消息。`send()` 方法不会阻塞调用线程。
> - 若通道已关闭，调用 `send()` 会以错误中止（因此它返回 `Result`）。当接收端被丢弃时，通道关闭。

