+++
title = "2.1 普通线程"
date = 2026-08-11T11:30:00+08:00
weight = 346
type = "docs"
description = "01-普通线程 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/threads/plain.html](https://google.github.io/comprehensive-rust/concurrency/threads/plain.html)

# 2.1 普通线程

Rust 线程的工作方式与其他语言中的线程类似：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::thread;
use std::time::Duration;

fn main() {
    thread::spawn(|| {
        for i in 0..10 {
            println!("Count in thread: {i}!");
            thread::sleep(Duration::from_millis(5));
        }
    });

    for i in 0..5 {
        println!("Main thread: {i}");
        thread::sleep(Duration::from_millis(5));
    }
}
```

- 派生新线程并不会在 `main` 结束时自动推迟程序终止。
- 各线程的 panic 彼此独立。
  - Panic 可以携带载荷，可用 [`Any::downcast_ref`] 解包。

> - 运行示例。
>   - 5ms 的时间间隔足够宽松，主线程与派生线程大体能保持同步。
>   - 注意：派生线程还没数到 10，程序就结束了！
>   - 因为 `main` 结束会终止整个程序，派生线程不会让程序继续存活。
>     - 若需要可与 `pthreads` / C++ `std::thread` / `boost::thread` 对比。
>
> - 如何等待派生线程完成？
> - [`thread::spawn`] 返回 `JoinHandle`。查阅文档。
>   - `JoinHandle` 有阻塞的 [`.join()`] 方法。
>
> - 使用 `let handle = thread::spawn(...)`，稍后调用 `handle.join()` 等待线程结束，让程序一直数到 10。
>
> - 若想返回一个值呢？
> - 再看文档：
>   - [`thread::spawn`] 的闭包返回 `T`
>   - `JoinHandle` 的 [`.join()`] 返回 `thread::Result<T>`
>
> - 用 `handle.join()` 的 `Result` 返回值来取得返回值。
>
> - 另一种情况呢？
>   - 在线程中触发 panic。注意这不会让 `main` panic。
>   - 访问 panic 载荷。这是讨论 [`Any`] 的好时机。
>
> - 现在可以从线程返回值了！那输入呢？
>   - 在线程闭包中按引用捕获某个值。
>   - 错误信息会提示我们必须移动它。
>   - 移入后，可以看到我们可以计算并返回派生值。
>
> - 若想借用呢？
>   - `main` 返回时会结束子线程，但另一个函数只会返回并留下它们继续运行。
>   - 那会是栈上的 use-after-return，违反内存安全！
>   - 如何避免？见下一页。
>
> [`Any`]: https://doc.rust-lang.org/std/any/index.html
> [`Any::downcast_ref`]: https://doc.rust-lang.org/std/any/trait.Any.html#method.downcast_ref
> [`thread::spawn`]: https://doc.rust-lang.org/std/thread/fn.spawn.html
> [`.join()`]: https://doc.rust-lang.org/std/thread/struct.JoinHandle.html#method.join

