+++
title = "3.2.6 forget 与 drop 函数"
date = 2026-08-11T11:30:00+08:00
weight = 436
type = "docs"
description = "06-forget 与 drop 函数 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/raii/forget_and_drop.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/raii/forget_and_drop.html)

# 3.2.6 forget 与 drop 函数

下面是
[`drop()`](https://doc.rust-lang.org/std/mem/fn.drop.html)
与
[`forget()`](https://doc.rust-lang.org/std/mem/fn.forget.html)
函数的签名：

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
// std::mem::forget
fn forget<T>(t: T) {
    let _ = std::mem::ManuallyDrop::new(t);
}

// std::mem::drop
fn drop<T>(_x: T) {}
```

> - `mem::forget()` 与 `mem::drop()` 都取得值 `t` 的所有权。
>
> - 尽管函数签名相同，它们的效果相反：
>
>   - `forget()` 使用
>     [`ManuallyDrop`](https://doc.rust-lang.org/std/mem/struct.ManuallyDrop.html)
>     阻止调用析构函数 `Drop::drop()`。
>
>     这在实现 drop bomb 或主动退出析构行为等场景中很有用。
>
>     但要小心：该值独占拥有的任何资源（如堆分配内存或文件句柄）将处于不可达状态。
>
>   - `drop()` 是丢弃值的便捷函数。因为 `t` 被移入函数，会在父函数返回前自动被 drop，从而触发其 `Drop::drop()` 实现。

