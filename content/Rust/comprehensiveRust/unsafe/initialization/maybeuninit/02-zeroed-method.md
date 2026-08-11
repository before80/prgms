+++
title = "7.1.2 MaybeUninit::zeroed() 方法"
date = 2026-08-11T11:30:00+08:00
weight = 542
type = "docs"
description = "02-MaybeUninit::zeroed() 方法 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/initialization/maybeuninit/zeroed-method.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/initialization/maybeuninit/zeroed-method.html)

# 7.1.2 MaybeUninit::zeroed() 方法

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::mem::{MaybeUninit, transmute};

fn main() {
    let mut x = [const { MaybeUninit::<u32>::zeroed() }; 10];

    x[6].write(7);

    // SAFETY: `x` 的所有元素都已写入
    let x: [u32; 10] = unsafe { transmute(x) };
    println!("{x:?}")
}
```

> 「`MaybeUninit<T>::zeroed()` 是 `MaybeUninit<T>::uninit()` 的另一种构造函数。它指示编译器用零填充 `T` 的位。」
>
> 问：「尽管内存已被写入，类型仍是 `MaybeUninit<T>`。谁能想到原因？」
>
> 答：某些类型要求其值非零或非空。典型例子是引用，但这也适用于许多其他类型。考虑 `NonZeroUsize` 整数类型及其同族中的其他类型。

