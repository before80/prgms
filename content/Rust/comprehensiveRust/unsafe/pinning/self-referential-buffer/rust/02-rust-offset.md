+++
title = "8.7.2.2 使用整数偏移"
date = 2026-08-11T11:30:00+08:00
weight = 557
type = "docs"
description = "02-使用整数偏移 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/self-referential-buffer/rust-offset.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/self-referential-buffer/rust-offset.html)

# 8.7.2.2 使用整数偏移

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug)]
pub struct SelfReferentialBuffer {
    data: [u8; 1024],
    position: usize,
}

impl SelfReferentialBuffer {
    pub fn new() -> Self {
        SelfReferentialBuffer { data: [0; 1024], position: 0 }
    }

    pub fn read(&self, n_bytes: usize) -> &[u8] {
        let available = self.data.len().saturating_sub(self.position);
        let len = n_bytes.min(available);
        &self.data[self.position..self.position + len]
    }

    pub fn write(&mut self, bytes: &[u8]) {
        let available = self.data.len().saturating_sub(self.position);
        let len = bytes.len().min(available);
        self.data[self.position..self.position + len].copy_from_slice(&bytes[..len]);
        self.position += len;
    }
}
```

> 在 Rust 中，更惯用的做法是使用偏移变量，并在需要时创建引用。

