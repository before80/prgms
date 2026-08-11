+++
title = "7.1.1 未初始化数组"
date = 2026-08-11T11:30:00+08:00
weight = 541
type = "docs"
description = "01-未初始化数组 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/initialization/maybeuninit/arrays.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/initialization/maybeuninit/arrays.html)

# 7.1.1 未初始化数组

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::mem::MaybeUninit;
use std::ptr;

fn main() {
    let input = b"RUST";

    let mut buf = [const { MaybeUninit::<u8>::uninit() }; 2048];

    // 通过向内存写入值来初始化元素
    for (i, input_byte) in input.iter().enumerate() {
        unsafe {
            let dst = buf.as_mut_ptr().add(i);
            ptr::write((*dst).as_mut_ptr(), *input_byte);
        }
    }

    // 当数组的一部分已初始化时，
    // 可以使用 unsafe 将其隔离出来
    let ptr_to_init_subslice = buf.as_ptr() as *const u8;
    let init =
        unsafe { std::slice::from_raw_parts(ptr_to_init_subslice, input.len()) };
    let text = std::str::from_utf8(init).unwrap();
    println!("{text}");

    // 必须手动 drop 已初始化的元素
    for element in &mut buf[0..input.len()] {
        unsafe {
            element.assume_init_drop();
        }
    }
}
```

> 要创建未初始化内存的数组，可在 `const` 上下文中使用 `::uninit()` 构造函数。
>
> 按常规方式使用 `ptr::write` 来初始化值。
>
> `.assume_init()` 对数组并不那么好用。它要求每个值都已初始化，而在复用缓冲区时未必如此。本例使用指针隔离已初始化的字节，以创建字符串切片。
>
> 从部分初始化的数组创建子切片时，要注意所有权并正确实现 drop。提醒：`MaybeUninit<T>` 不会对内部的 `T` 调用 drop。
>
> `MaybeUninit<[u8;2048]>` 与 `[MaybeUninit::<u8>; 2048]` 是不同的。前者是「整块未初始化内存的数组」，后者是「元素可能未初始化的数组」。
>
> - `MaybeUninit<[u8;2048]>` 是「全有或全无」。要么完整初始化整个数组再调用 `assume_init`，要么保持为 `MaybeUninit<[u8; 2048]>` 且不要当作 `[u8; 2048]` 使用。
> - `[MaybeUninit<u8>; 2048]` 允许逐个初始化元素，然后取已初始化前缀的子切片，并通过 `std::slice::from_raw_parts` 将其视为 `[u8]`。
> - `slice_assume_init_ref` 仅当切片中每个元素都已初始化时才是安全的。在本例中，我们在恰好写入了那些字节之后，才传入 `&buf[..input.len()]`。
> - 当 `T` 需要 drop 时，必须为已初始化的元素手动调用 `assume_init_drop()`。跳过这一步会泄漏内存。然而，对未初始化的元素调用它会导致未定义行为。

