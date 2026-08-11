+++
title = "7.1.3 ptr::write 与赋值"
date = 2026-08-11T11:30:00+08:00
weight = 543
type = "docs"
description = "03-ptr::write 与赋值 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/initialization/maybeuninit/write-vs-assignment.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/initialization/maybeuninit/write-vs-assignment.html)

# 7.1.3 ptr::write 与赋值

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::mem::MaybeUninit;

fn main() {
    let mut buf = MaybeUninit::<String>::uninit();

    // 初始化
    buf.write(String::from("Hello, Rust!"));

    // 覆写
    buf.write(String::from("Hi again"));

    // 赋值会替换整个 MaybeUninit 值
    buf = MaybeUninit::new(String::from("Goodbye"));

    // 确保内部值被 drop
    let _ = unsafe { buf.assume_init() };
}
```

> 替换内部值可能导致内存泄漏，因为其 drop 语义与大多数类型不同。`MaybeUninit<T>` 不会对内部的 `T` 调用析构函数。
>
> `MaybeUninit::write()` 使用 `ptr::write`：它在原地初始化内存，不会读取或 drop 旧内容。当内存可能未初始化时，这正是你需要的；但若那里已有有效值，也会因此泄漏。
>
> 赋值，例如 `buf = MaybeUninit::new(value)`，会替换整个 `MaybeUninit`。旧的 `MaybeUninit` 被移动然后 drop，但 `MaybeUninit` 对 `T` 没有析构函数，因此内部值不会被 drop。若旧槽位持有已初始化的值，就会像 `write()` 一样泄漏。
>
> 若需要正常的 drop 行为，你需要通过 `assume_init` 或相关方法之一告知 Rust 该值已初始化。

