+++
title = "7.2 如何初始化内存"
date = 2026-08-11T11:30:00+08:00
weight = 544
type = "docs"
description = "01-如何初始化内存 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/initialization/how-to-initialize-memory.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/initialization/how-to-initialize-memory.html)

# 7.2 如何初始化内存

步骤：

1. 创建 `MaybeUninit<T>`
2. 向其中写入一个值
3. 通知 Rust 该内存已初始化

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::mem::MaybeUninit;

fn main() {
    // 步骤 1：创建 MaybeUninit
    let mut uninit = MaybeUninit::uninit();

    // 步骤 2：向内存写入有效值
    uninit.write(1);

    // 步骤 3：告知类型系统该内存位置已有效
    let init = unsafe { uninit.assume_init() };

    println!("{init}");
}
```

> 处理未初始化内存时，请遵循这一通用流程：创建、写入、确认。
>
> 1. 创建 `MaybeUninit<T>`。`::uninit()` 构造函数最为通用，但还有其他构造函数会在创建的同时完成写入。
>
> 2. 写入一个 `T` 类型的值。注意这可以在 safe Rust 中完成。留在 safe Rust 中很有用，因为你必须确保写入的值是有效的。
>
> 3. 通过 `.assume_init()` 方法向类型系统确认内存现已初始化。

