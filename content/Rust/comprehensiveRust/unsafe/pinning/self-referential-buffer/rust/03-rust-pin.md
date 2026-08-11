+++
title = "8.7.2.3 使用 `Pin<Ptr>`"
date = 2026-08-11T11:30:00+08:00
weight = 558
type = "docs"
description = "03-使用 `Pin<Ptr>` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/self-referential-buffer/rust-pin.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/self-referential-buffer/rust-pin.html)

# 8.7.2.3 使用 `Pin<Ptr>`

Pinning 允许 Rust 程序员创建与 C++ 类更为相似的类型。

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::marker::PhantomPinned;
use std::pin::Pin;

/// 不可移动的自引用缓冲区。
#[derive(Debug)]
pub struct SelfReferentialBuffer {
    data: [u8; 1024],
    cursor: *mut u8,
    _pin: PhantomPinned,
}

impl SelfReferentialBuffer {
    pub fn new() -> Pin<Box<Self>> {
        let buffer = SelfReferentialBuffer {
            data: [0; 1024],
            cursor: std::ptr::null_mut(),
            _pin: PhantomPinned,
        };
        let mut pinned = Box::pin(buffer);

        unsafe {
            let mut_ref = Pin::get_unchecked_mut(pinned.as_mut());
            mut_ref.cursor = mut_ref.data.as_mut_ptr();
        }

        pinned
    }

    pub fn read(&self, n_bytes: usize) -> &[u8] {
        unsafe {
            let start = self.data.as_ptr();
            let end = start.add(self.data.len());
            let cursor = self.cursor as *const u8;

            assert!((start..=end).contains(&cursor), "cursor is out of bounds");

            let offset = cursor.offset_from(start) as usize;
            let available = self.data.len().saturating_sub(offset);
            let len = n_bytes.min(available);

            &self.data[offset..offset + len]
        }
    }

    pub fn write(mut self: Pin<&mut Self>, bytes: &[u8]) {
        let this = unsafe { self.as_mut().get_unchecked_mut() };
        unsafe {
            let start = this.data.as_mut_ptr();
            let end = start.add(1024);

            assert!((start..=end).contains(&this.cursor), "cursor is out of bounds");
            let available = end.offset_from(this.cursor) as usize;
            let len = bytes.len().min(available);

            std::ptr::copy_nonoverlapping(bytes.as_ptr(), this.cursor, len);
            this.cursor = this.cursor.add(len);
        }
    }
}
```

> 注意函数签名现已改变。例如 `::new()` 返回 `Pin<Box<Self>>` 而非 `Self`。这会产生堆分配，因为 `Pin<Ptr>` 必须与 `Box` 等指针类型配合使用。
>
> 在 `::new()` 中，我们在 _固定之后_ 使用 `Pin::get_unchecked_mut()` 获取缓冲区的可变引用。这是 `unsafe` 的，因为我们暂时打破了 pinning 保证以初始化 `cursor`。此后必须确保不再移动 `SelfReferentialBuffer`。`Pin` 的安全约定是：一旦值被固定，其内存位置在 drop 之前保持不变。

