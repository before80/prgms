+++
title = "7.3 部分初始化"
date = 2026-08-11T11:30:00+08:00
weight = 545
type = "docs"
description = "02-部分初始化 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/initialization/partial-initialization.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/initialization/partial-initialization.html)

# 7.3 部分初始化

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::mem::MaybeUninit;

fn main() {
    // let mut buf = [0u8; 2048];
    let mut buf = [const { MaybeUninit::<u8>::uninit() }; 2048];

    let external_data = b"Hello, Rust!";
    let len = external_data.len();

    for (dest, src) in buf.iter_mut().zip(external_data) {
        dest.write(*src);
    }

    // SAFETY: 我们恰好用 UTF-8 文本初始化了 `buf` 中的 `len` 个字节
    let text: &str = unsafe {
        let ptr: *const u8 = buf.as_ptr().cast::<u8>();
        let init: &[u8] = std::slice::from_raw_parts(ptr, len);
        std::str::from_utf8_unchecked(init)
    };

    println!("{text}");
}
```

> 这段代码模拟从某个外部源接收数据。
>
> 将字节从外部源读入缓冲区时，你通常不知道会收到多少字节。使用 `MaybeUninit<T>` 可以只分配一次缓冲区，而无需为冗余的初始化遍历付出代价。
>
> 若用标准语法创建数组（`buf = [0u8; 2048]`），整个缓冲区会被零填充。`MaybeUninit<T>` 告诉编译器预留空间，但暂时不要触碰内存。
>
> 问：代码片段中哪一部分扮演着与 `.assume_init()` 类似的角色？\
> 答：指针转换和隐式读取。
>
> 我们不能对整个数组调用 `assume_init()`。那样是不健全的，因为大多数元素仍未初始化。相反，我们将指针从 `*const MaybeUninit<u8>` 转换为 `*const u8`，并构建一个仅覆盖已初始化部分的切片。

