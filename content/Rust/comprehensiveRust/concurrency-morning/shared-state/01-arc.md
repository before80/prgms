+++
title = "5.1 `Arc`"
date = 2026-08-11T11:30:00+08:00
weight = 358
type = "docs"
description = "01-`Arc` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/shared-state/arc.html](https://google.github.io/comprehensive-rust/concurrency/shared-state/arc.html)

# 5.1 `Arc`

[`Arc<T>`][1] 通过 `Arc::clone` 允许共享的只读所有权：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::sync::Arc;
use std::thread;

/// 打印是哪个线程丢弃了它的结构体。
#[derive(Debug)]
struct WhereDropped(Vec<i32>);

impl Drop for WhereDropped {
    fn drop(&mut self) {
        println!("Dropped by {:?}", thread::current().id())
    }
}

fn main() {
    let v = Arc::new(WhereDropped(vec![10, 20, 30]));
    let mut handles = Vec::new();
    for i in 0..5 {
        let v = Arc::clone(&v);
        handles.push(thread::spawn(move || {
            // 休眠 0–500ms。
            std::thread::sleep(std::time::Duration::from_millis(500 - i * 100));
            let thread_id = thread::current().id();
            println!("{thread_id:?}: {v:?}");
        }));
    }

    // 现在只有派生出的线程持有 `v` 的克隆。
    drop(v);

    // 当最后一个派生线程结束时，它会丢弃 `v` 的内容。
    handles.into_iter().for_each(|h| h.join().unwrap());
}
```

[1]: https://doc.rust-lang.org/std/sync/struct.Arc.html

> - `Arc` 表示 “Atomic Reference Counted”（原子引用计数），是使用原子操作的线程安全版 `Rc`。
> - 无论 `T` 是否实现 `Clone`，`Arc<T>` 都实现 `Clone`。当且仅当 `T` 同时实现 `Send` 与 `Sync` 时，它才实现 `Send` 与 `Sync`。
> - `Arc::clone()` 的代价是执行原子操作，之后使用 `T` 是免费的。
> - 当心引用环，`Arc` 不会用垃圾回收来检测它们。
>   - `std::sync::Weak` 可以帮忙。

