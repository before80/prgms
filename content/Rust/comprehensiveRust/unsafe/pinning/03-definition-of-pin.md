+++
title = "8.3 Pin<Ptr> 的定义"
date = 2026-08-11T11:30:00+08:00
weight = 549
type = "docs"
description = "03-Pin<Ptr> 的定义 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/definition-of-pin.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/definition-of-pin.html)

# 8.3 Pin<Ptr> 的定义

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[repr(transparent)]
pub struct Pin<Ptr> {
    pointer: Ptr,
}

impl<Ptr: Deref<Target: Unpin>> Pin<Ptr> {
    pub fn new(pointer: Ptr) -> Pin<Ptr> { ... }
}

impl<Ptr: Deref> Pin<Ptr> {
    pub unsafe fn new_unchecked(pointer: Ptr) -> Pin<Ptr> { ... }
}
```

> `Pin` 是对 _指针类型_ 的最小包装；指针类型定义为实现了 `Deref` 的类型。
>
> 然而，`Pin::new()` 只接受解引用目标实现了 `Unpin` 的类型（`Deref<Target: Unpin>`）。这使 `Pin` 能够依赖类型系统来强制其保证。
>
> 未实现 `Unpin` 的类型——即需要 pinning 的类型——必须通过 unsafe 的 `Pin::new_unchecked()` 创建 `Pin`。
>
> 旁注：与其他 `new()`/`new_unchecked()` 方法对不同，`new` 不做任何运行时检查。检查是零成本的编译期检查。

