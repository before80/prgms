+++
title = "2.2 Futures"
date = 2026-08-11T11:30:00+08:00
weight = 369
type = "docs"
description = "02-Futures — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/async/futures.html](https://google.github.io/comprehensive-rust/concurrency/async/futures.html)

# 2.2 Futures

[`Future`](https://doc.rust-lang.org/std/future/trait.Future.html) 是一个 trait，由表示可能尚未完成的操作的对象实现。可以对 future 进行轮询，`poll` 返回
[`Poll`](https://doc.rust-lang.org/std/task/enum.Poll.html)。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::pin::Pin;
use std::task::Context;

pub trait Future {
    type Output;
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}

pub enum Poll<T> {
    Ready(T),
    Pending,
}
```

async 函数返回 `impl Future`。也可以（但不常见）为自己的类型实现 `Future`。例如，`tokio::spawn` 返回的 `JoinHandle` 实现了 `Future`，以便对其 join。

对 Future 使用 `.await` 关键字，会使当前 async 函数暂停，直到该 Future 就绪，然后求值为其输出。

> - `Future` 与 `Poll` 类型的实现与所示完全一致；点击链接可在文档中查看实现。
>
> - `Context` 允许 Future 在超时等事件发生时，安排自己再次被轮询。
>
> - `Pin` 确保 Future 不会在内存中移动，从而使指向该 future 的指针保持有效。这是为了让引用在 `.await` 之后仍然有效。我们将在「陷阱」部分讨论 `Pin`。

