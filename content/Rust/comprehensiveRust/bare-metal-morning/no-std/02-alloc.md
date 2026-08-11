+++
title = "2.2 `alloc`"
date = 2026-08-11T11:30:00+08:00
weight = 297
type = "docs"
description = "02-`alloc` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/alloc.html](https://google.github.io/comprehensive-rust/bare-metal/alloc.html)

# 2.2 `alloc`

要使用 `alloc`，必须实现一个
[全局（堆）分配器](https://doc.rust-lang.org/stable/std/alloc/trait.GlobalAlloc.html)。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#![no_main]
#![no_std]

extern crate alloc;
extern crate panic_halt as _;

use alloc::string::ToString;
use alloc::vec::Vec;
use buddy_system_allocator::LockedHeap;

#[global_allocator]
static HEAP_ALLOCATOR: LockedHeap<32> = LockedHeap::<32>::new();

const HEAP_SIZE: usize = 65536;
static mut HEAP: [u8; HEAP_SIZE] = [0; HEAP_SIZE];

pub fn entry() {
    // SAFETY: `HEAP` 仅在此处使用，且 `entry` 只调用一次。
    unsafe {
        // 给分配器一些可分配的内存。
        HEAP_ALLOCATOR.lock().init(&raw mut HEAP as usize, HEAP_SIZE);
    }

    // 现在可以做需要堆分配的事情了。
    let mut v = Vec::new();
    v.push("A string".to_string());
}
```

> - `buddy_system_allocator` 是一个实现基本 buddy system 分配器的 crate。也有其他 crate，或者你可以写自己的，或接到已有分配器上。
> - `LockedHeap` 的 const 参数是分配器的最大阶（max order）；本例中最多可分配 2**32 字节的区域。
> - 若依赖树中任何 crate 依赖 `alloc`，则二进制中必须恰好定义一个全局分配器。通常放在顶层二进制 crate 里。
> - `extern crate panic_halt as _` 是为了确保链接进 `panic_halt` crate，从而得到它的 panic handler。
> - 本示例可以构建但不能运行，因为没有入口点。

