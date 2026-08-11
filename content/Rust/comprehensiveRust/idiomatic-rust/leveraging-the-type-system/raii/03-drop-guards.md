+++
title = "3.2.3 Drop Guard"
date = 2026-08-11T11:30:00+08:00
weight = 433
type = "docs"
description = "03-Drop Guard — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/raii/drop_guards.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/raii/drop_guards.html)

# 3.2.3 Drop Guard

Rust 中的 **drop guard** 是一个临时对象，在离开作用域时执行某种清理。对于 `Mutex`，`lock` 方法返回一个 `MutexGuard`，在 `drop` 时自动解锁互斥锁：

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
struct Mutex {
    is_locked: bool,
}

struct MutexGuard<'a> {
    mutex: &'a mut Mutex,
}

impl Mutex {
    fn new() -> Self {
        Self { is_locked: false }
    }

    fn lock(&mut self) -> MutexGuard<'_> {
        self.is_locked = true;
        MutexGuard { mutex: self }
    }
}

impl Drop for MutexGuard<'_> {
    fn drop(&mut self) {
        self.mutex.is_locked = false;
    }
}
```

> - 上例展示了简化版的 `Mutex` 及其关联的 guard。
>
> - 尽管不是生产就绪的实现，它说明了核心思想：
>
>   - guard 代表独占访问，
>   - 其 `Drop` 实现在离开作用域时释放锁。
>
> ## 深入探索
>
> 本示例展示的是 C++ 风格的互斥锁：不包含它所保护的数据。这在 Rust 中并不地道，此处目标只是说明 drop guard 的核心思想，而非演示正确的 Rust 互斥锁设计。
>
> 为简洁起见，省略了若干特性：
>
> - 真正的 `Mutex<T>` 把受保护的值存在互斥锁内部。\
>   这个玩具示例完全省略了该值，只聚焦 drop guard 机制。
> - 通过 `MutexGuard` 上的 `Deref` 与 `DerefMut` 提供符合人体工学的访问（让 guard 表现得像 `&T` 或 `&mut T`）。
> - 完整的阻塞式 `.lock()` 方法以及非阻塞的 `try_lock` 变体。
>
> 可参考
> [Rust 标准库中的 `Mutex` 实现](https://doc.rust-lang.org/std/sync/struct.Mutex.html)
> 作为生产就绪互斥锁的例子。
> [`parking_lot` crate 中的 `Mutex`](https://docs.rs/parking_lot/latest/parking_lot/type.Mutex.html)
> 也是值得一看的参考。

