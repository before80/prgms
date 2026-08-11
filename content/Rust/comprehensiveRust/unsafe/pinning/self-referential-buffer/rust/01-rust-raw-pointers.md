+++
title = "8.7.2.1 使用原始指针"
date = 2026-08-11T11:30:00+08:00
weight = 556
type = "docs"
description = "01-使用原始指针 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/self-referential-buffer/rust-raw-pointers.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/self-referential-buffer/rust-raw-pointers.html)

# 8.7.2.1 使用原始指针

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug)]
pub struct SelfReferentialBuffer {
    data: [u8; 1024],
    cursor: *mut u8,
}

impl SelfReferentialBuffer {
    pub fn new() -> Self {
        let mut buffer =
            SelfReferentialBuffer { data: [0; 1024], cursor: std::ptr::null_mut() };

        buffer.update_cursor();
        buffer
    }

    // 危险：每次移动后都必须调用
    pub fn update_cursor(&mut self) {
        self.cursor = self.data.as_mut_ptr();
    }

    pub fn read(&self, n_bytes: usize) -> &[u8] {
        unsafe {
            let start = self.data.as_ptr();
            let end = start.add(1024);
            let cursor = self.cursor as *const u8;

            assert!((start..=end).contains(&cursor), "cursor is out of bounds");

            let available = end.offset_from(cursor) as usize;
            let len = n_bytes.min(available);
            std::slice::from_raw_parts(cursor, len)
        }
    }

    pub fn write(&mut self, bytes: &[u8]) {
        unsafe {
            let start = self.data.as_mut_ptr();
            let end = start.add(1024);

            assert!((start..=end).contains(&self.cursor), "cursor is out of bounds");
            let available = end.offset_from(self.cursor) as usize;
            let len = bytes.len().min(available);

            std::ptr::copy_nonoverlapping(bytes.as_ptr(), self.cursor, len);
            self.cursor = self.cursor.add(len);
        }
    }
}
```

> 不要在此停留太久。
>
> 讨论要点：
>
> - 强调 `unsafe` 频繁出现。这暗示另一种设计可能更合适。
> - `unsafe` 块缺少 safety 注释。因此，这段代码是不健全的。
> - `unsafe` 块范围过大。良好实践是使用更小的 `unsafe` 块，并明确行为、前置条件与 safety 注释。
>
> 问题：
>
> 问：`read()` 和 `write()` 方法是否应标记为 unsafe？\
> 答：是的，因为除非写入，`self.cursor` 将是空指针。

