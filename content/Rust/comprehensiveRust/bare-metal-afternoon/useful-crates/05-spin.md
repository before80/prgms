+++
title = "2.5 `旋转`"
date = 2026-08-11T11:30:00+08:00
weight = 337
type = "docs"
description = "05-`旋转` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/useful-crates/spin.html](https://google.github.io/comprehensive-rust/bare-metal/useful-crates/spin.html)

# 2.5 `旋转`

`std::sync::Mutex` 和 `std::sync` 中的其他同步原语是
在“core”或“alloc”中不可用。我们如何管理同步或
内部可变性，例如在不同 CPU 之间共享状态？

[`spin`][1] 箱提供了其中许多基于自旋锁的等价物
基元。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use spin::mutex::SpinMutex;

static COUNTER: SpinMutex<u32> = SpinMutex::new(0);

fn main() {
    dbg!(COUNTER.lock());
    *计数器.lock() += 2;
    dbg!(COUNTER.lock());
}
```

> - 如果在中断处理程序中锁定，请小心避免死锁。
> - `spin` 也有票锁互斥体实现；相当于“RwLock”，
>   来自“std::sync”的“Barrier”和“Once”；和“Lazy”用于延迟初始化。
> - [`once_cell`][2] 板条箱还具有一些用于后期初始化的有用类型
>   与 `spin::once::Once` 的方法略有不同。
> - Rust Playground 包含 `spin`，因此这个示例可以很好地内联运行。


[1]: https://crates.io/crates/spin
[2]: https://crates.io/crates/once_cell
