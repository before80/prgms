+++
title = "2.1 `async`/`await`"
date = 2026-08-11T11:30:00+08:00
weight = 368
type = "docs"
description = "01-`async`/`await` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/async/async-await.html](https://google.github.io/comprehensive-rust/concurrency/async/async-await.html)

# 2.1 `async`/`await`

从高层看，异步 Rust 代码看起来很像「普通」顺序代码：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use futures::executor::block_on;

async fn count_to(count: i32) {
    for i in 0..count {
        println!("Count is: {i}!");
    }
}

async fn async_main(count: i32) {
    count_to(count).await;
}

fn main() {
    block_on(async_main(10));
}
```

> 要点：
>
> - 注意这是展示语法的简化示例。其中没有长时间运行的操作，也没有真正的并发！
>
> - `async` 关键字是语法糖。编译器会把返回类型替换成 future。
>
> - 不能把 `main` 做成 async，除非额外指示编译器如何使用返回的 future。
>
> - 需要 executor 来运行异步代码。`block_on` 会阻塞当前线程，直到所提供的 future 运行完成。
>
> - `.await` 异步等待另一操作完成。与 `block_on` 不同，`.await` 不会阻塞当前线程。
>
> - `.await` 只能用在 `async` 函数（或块；稍后介绍）内部。

