+++
title = "6.1 哲学家就餐"
date = 2026-08-11T11:30:00+08:00
weight = 362
type = "docs"
description = "01-哲学家就餐 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/sync-exercises/dining-philosophers.html](https://google.github.io/comprehensive-rust/concurrency/sync-exercises/dining-philosophers.html)

# 6.1 哲学家就餐

哲学家就餐问题是并发领域的经典问题：

> 五位哲学家同桌用餐。每位哲学家有自己的座位。每两个盘子之间有一根筷子。菜是意大利面，需要两根筷子才能吃。每位哲学家只能交替思考与进食。而且，只有同时拿到左右两根筷子时，哲学家才能吃面。因此，只有当左右邻居都在思考、而不是在进食时，两根筷子才可用。某位哲学家吃完后，会放下两根筷子。

本练习需要本地 [Cargo 安装](../../cargo/running-locally.md)。把下面的代码复制到 `src/main.rs`，填空，并测试 `cargo run` 不会死锁：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::sync::{Arc, Mutex, mpsc};
use std::thread;
use std::time::Duration;

struct Chopstick;

struct Philosopher {
    name: String,
    // left_chopstick: ...
    // right_chopstick: ...
    // thoughts: ...
}

impl Philosopher {
    fn think(&self) {
        self.thoughts
            .send(format!("Eureka! {} has a new idea!", &self.name))
            .unwrap();
    }

    fn eat(&self) {
        // 拿起筷子……
        println!("{} is eating...", &self.name);
        thread::sleep(Duration::from_millis(10));
    }
}

static PHILOSOPHERS: &[&str] =
    &["Socrates", "Hypatia", "Plato", "Aristotle", "Pythagoras"];

fn main() {
    // 创建筷子

    // 创建哲学家

    // 让他们每人思考并进食 100 次

    // 输出他们的想法
}
```

可以使用如下 `Cargo.toml`：

```toml
[package]
name = "dining-philosophers"
version = "0.1.0"
edition = "2024"
```

> - 鼓励学员先专注实现一个「大体」能工作的方案。
> - 最简单方案中的死锁是一类通用并发问题，也说明 Rust 并不会自动防止这类缺陷。

