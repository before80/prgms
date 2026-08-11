+++
title = "5.1 哲学家就餐 — 异步"
date = 2026-08-11T11:30:00+08:00
weight = 384
type = "docs"
description = "01-哲学家就餐 — 异步 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/async-exercises/dining-philosophers.html](https://google.github.io/comprehensive-rust/concurrency/async-exercises/dining-philosophers.html)

# 5.1 哲学家就餐 — 异步

问题描述见[哲学家就餐](../sync-exercises/dining-philosophers.md)。

与之前一样，本练习需要本地 [Cargo 安装](../../cargo/running-locally.md)。把下面的代码复制到 `src/main.rs`，填空，并测试 `cargo run` 不会死锁：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::sync::Arc;
use tokio::sync::{Mutex, mpsc};
use tokio::time;

struct Chopstick;

struct Philosopher {
    name: String,
    // left_chopstick: ...
    // right_chopstick: ...
    // thoughts: ...
}

impl Philosopher {
    async fn think(&self) {
        self.thoughts
            .send(format!("Eureka! {} has a new idea!", &self.name))
            .await
            .unwrap();
    }

    async fn eat(&self) {
        // 一直尝试直到拿到两根筷子
        // 拿起筷子……

        println!("{} is eating...", &self.name);
        time::sleep(time::Duration::from_millis(5)).await;

        // 锁在此处丢弃
    }
}

// tokio 调度器在 5 位哲学家时不会死锁，因此用 2 位。
static PHILOSOPHERS: &[&str] = &["Socrates", "Hypatia"];

#[tokio::main]
async fn main() {
    // 创建筷子

    // 创建哲学家

    // 让他们思考并进食

    // 输出他们的想法
}
```

这次使用异步 Rust，因此需要 `tokio` 依赖。可以使用如下 `Cargo.toml`：

```toml
[package]
name = "dining-philosophers-async-dine"
version = "0.1.0"
edition = "2024"

[dependencies]
tokio = { version = "1.26.0", features = ["sync", "time", "macros", "rt-multi-thread"] }
```

另请注意：这次必须使用 `tokio` crate 中的 `Mutex` 与 `mpsc` 模块。

> - 你能做成单线程实现吗？

