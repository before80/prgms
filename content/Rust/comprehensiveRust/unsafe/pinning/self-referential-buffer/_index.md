+++
title = "8.7 自引用缓冲区示例"
date = 2026-08-11T11:30:00+08:00
weight = 553
type = "docs"
description = "自引用缓冲区示例 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/self-referential-buffer.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/self-referential-buffer.html)

# 8.7 自引用缓冲区示例

「自引用缓冲区（self-referential buffer）」是包含指向自身某个字段的引用的类型：

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub struct SelfReferentialBuffer {
    data: [u8; 1024],
    cursor: *mut u8,
}
```

这类结构在 Rust 中并不典型，因为当 `SelfReferentialBuffer` 的实例移动时，无法更新 cursor 的地址。

然而，在提供垃圾回收的其他语言中，以及允许用户在移动和拷贝时自定义行为的 C++ 中，这种写法更为自然。

## 大纲

本小节约需 1 小时 20 分钟。内容包括：

| 内容 | 时长 |
| --- | --- |
| 什么是 pinning | 5 分钟 |
| Pin<Ptr> 的定义 | 5 分钟 |
| `PhantomPinned` 标记类型 | 5 分钟 |
| 自引用缓冲区示例 | 50 分钟 |
| `Pin<Ptr>` 与 `Drop` | 15 分钟 |

