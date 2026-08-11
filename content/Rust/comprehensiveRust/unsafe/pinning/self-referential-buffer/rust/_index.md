+++
title = "8.7.2 Rust 建模"
date = 2026-08-11T11:30:00+08:00
weight = 555
type = "docs"
description = "Rust 建模 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/self-referential-buffer/rust.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/self-referential-buffer/rust.html)

# 8.7.2 Rust 建模

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 原始指针
pub struct SelfReferentialBuffer {
    data: [u8; 1024],
    cursor: *mut u8,
}

/// 整数偏移
pub struct SelfReferentialBuffer {
    data: [u8; 1024],
    cursor: usize,
}

/// Pinning
pub struct SelfReferentialBuffer {
    data: [u8; 1024],
    cursor: *mut u8,
    _pin: std::marker::PhantomPinned,
}
```

## 供参考的原始 C++ 类定义

```cpp,ignore
class SelfReferentialBuffer {
    char data[1024];
    char* cursor;
};
```

> 接下来几页展示三种在 Rust 中创建与原始 C++ 语义相同类型的方法。
>
> - 使用原始指针：与 C++ 非常接近，但使用所得类型极其危险
> - 存储整数偏移：在 Rust 中更自然，但引用需要手动创建
> - Pinning：允许使用原始指针，且 `unsafe` 块更少

