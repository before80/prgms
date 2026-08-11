+++
title = "3.2.2 互斥锁"
date = 2026-08-11T11:30:00+08:00
weight = 432
type = "docs"
description = "02-互斥锁 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/raii/mutex.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/raii/mutex.html)

# 3.2.2 互斥锁

在先前的示例中，RAII 用于管理文件描述符等具体资源。对于 `Mutex`，「资源」是对值的可变访问。你通过调用 `lock` 访问该值，它返回一个 `MutexGuard`，在 drop 时会自动解锁 `Mutex`。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::sync::Mutex;

fn main() {
    let m = Mutex::new(vec![1, 2, 3]);

    let mut guard = m.lock().unwrap();
    guard.push(4);
    guard.push(5);
    println!("{guard:?}");
}
```

> - `Mutex` 控制对值的独占访问。与先前的 RAII 示例不同，这里的资源是逻辑上的：对内部数据的临时独占访问权。
>
> - 该权利由 `MutexGuard` 表示。同一时刻只能存在一个针对该互斥锁的 guard。在它存活期间，提供 `&mut T` 访问。
>
> - 虽然 `lock()` 接受 `&self`，却返回带有可变访问的 `MutexGuard`。这通过**内部可变性**（interior mutability）实现：类型在内部管理自己的借用规则，从而允许通过 `&self` 进行修改。
>
> - `MutexGuard` 实现了 `Deref` 和 `DerefMut`，使访问很符合人体工学。你锁定互斥锁，然后像使用 `&mut T` 一样使用 guard。
>
> - 互斥锁由 `MutexGuard::drop()` 释放。你从不调用显式的 unlock 函数。

