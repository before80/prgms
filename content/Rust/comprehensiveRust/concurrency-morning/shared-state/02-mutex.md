+++
title = "5.2 `Mutex`"
date = 2026-08-11T11:30:00+08:00
weight = 359
type = "docs"
description = "02-`Mutex` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/shared-state/mutex.html](https://google.github.io/comprehensive-rust/concurrency/shared-state/mutex.html)

# 5.2 `Mutex`

[`Mutex<T>`][1] 确保互斥，并允许在只读接口背后对 `T` 进行可变访问（[内部可变性](../../borrowing/interior-mutability.md)的另一种形式）：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::sync::Mutex;

fn main() {
    let v = Mutex::new(vec![10, 20, 30]);
    println!("v: {:?}", v.lock().unwrap());

    {
        let mut guard = v.lock().unwrap();
        guard.push(40);
    }

    println!("v: {:?}", v.lock().unwrap());
}
```

注意我们有一个 [`impl<T: Send> Sync for Mutex<T>`][2] 的 blanket 实现。

[1]: https://doc.rust-lang.org/std/sync/struct.Mutex.html
[2]: https://doc.rust-lang.org/std/sync/struct.Mutex.html#impl-Sync-for-Mutex%3CT%3E
[3]: https://doc.rust-lang.org/std/sync/struct.Arc.html

> - Rust 中的 `Mutex` 看起来像只有一个元素的集合——受保护的数据。
>   - 不可能忘记在访问受保护数据之前获取互斥锁。
> - 你可以通过加锁从 `&Mutex<T>` 得到 `&mut T`。`MutexGuard` 确保 `&mut T` 不会在锁持有期之外存活。
> - 当且仅当 `T` 实现 `Send` 时，`Mutex<T>` 同时实现 `Send` 与 `Sync`。
> - 读写锁对应物：`RwLock`。
> - 为什么 `lock()` 返回 `Result`？
>   - 若持有 `Mutex` 的线程 panic 了，`Mutex` 会变成「中毒」（poisoned），以表明它保护的数据可能处于不一致状态。对中毒的互斥锁调用 `lock()` 会以 [`PoisonError`] 失败。你可以在错误上调用 `into_inner()` 无论如何恢复数据。
>
> [`PoisonError`]: https://doc.rust-lang.org/std/sync/struct.PoisonError.html

