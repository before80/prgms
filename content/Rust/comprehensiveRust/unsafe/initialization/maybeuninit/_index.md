+++
title = "7.1 MaybeUninit<T>（可能未初始化）"
date = 2026-08-11T11:30:00+08:00
weight = 540
type = "docs"
description = "MaybeUninit<T>（可能未初始化） — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/initialization/maybeuninit.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/initialization/maybeuninit.html)

# 7.1 MaybeUninit<T>（可能未初始化）

`MaybeUninit<T>` 允许 Rust 引用未初始化的内存。

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::mem::MaybeUninit;

fn main() {
    let uninit = MaybeUninit::<&i32>::uninit();
    println!("{uninit:?}");
}
```

> 「Safe Rust 无法引用可能未初始化的数据。」
>
> 「然而，所有数据进入程序时都是未初始化的。」
>
> 「因此，我们需要类型系统中的某种桥梁，让内存能够完成过渡。`MaybeUninit<T>` 就是这种类型。」
>
> 「`MaybeUninit<T>` 与 `Option<T>` 类型非常相似，尽管语义截然不同。对 `MaybeUninit<T>` 而言，`Option::None` 的等价物是未初始化内存，而向其中写入是安全的。」
>
> 「从可能未初始化的内存中读取极其危险。」

