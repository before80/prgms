+++
title = "3.6.2 带数据的令牌类型：Mutex Guard"
date = 2026-08-11T11:30:00+08:00
weight = 463
type = "docs"
description = "02-带数据的令牌类型：Mutex Guard — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/token-types/mutex-guard.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/token-types/mutex-guard.html)

# 3.6.2 带数据的令牌类型：Mutex Guard

有时，令牌类型需要附加数据。Mutex guard 是代表「权限 + 数据」的令牌示例。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::sync::{Arc, Mutex, MutexGuard};

fn main() {
    let mutex = Arc::new(Mutex::new(42));
    let try_mutex_guard: Result<MutexGuard<'_, _>, _> = mutex.lock();
    if let Ok(mut guarded) = try_mutex_guard {
        // 取得的 MutexGuard 是独占访问的证明。
        *guarded = 451;
    }
}
```

> - 互斥锁强制对值的读/写访问互斥。我们在本课程前面已介绍过互斥锁（参见：RAII/Mutex），但这里我们专门看 `MutexGuard`。
>
> - `MutexGuard` 是由 `Mutex` 生成的值，证明你在该时刻拥有读/写访问权。
>
>   `MutexGuard` 还持有对生成它的 `Mutex` 的引用，并通过 `Deref` 与 `DerefMut` 实现对 `Mutex` 数据的访问，同时底层 `Mutex` 对该用户保持数据私有。
>
> - 若 `mutex.lock()` 不返回 `MutexGuard`，你就没有权限修改互斥锁内的值。
>
>   你不仅没有权限，而且除非获得 `MutexGuard`，否则没有任何手段访问互斥锁数据。
>
>   这与 C++ 形成对比：C++ 中互斥锁与 lock guard 并不控制对数据本身的访问，只充当用户每次读或操作数据时必须记得检查的标志。
>
> - 演示：将 `mutex` 变量设为可变，然后尝试解引用以修改其值。展示它没有 deref 实现，且除了取得 mutex guard 外没有其他方式拿到其持有的数据。

