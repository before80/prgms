+++
title = "5.2 复制内存"
date = 2026-08-11T11:30:00+08:00
weight = 527
type = "docs"
description = "复制内存 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/copying-memory.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/copying-memory.html)

# 5.2 复制内存

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 从 `source` 读取字节并写入 `dest`
pub fn copy(dest: &mut [u8], source: &[u8]) { ... }
```

> 「这是我们最初的函数原型。」
>
> 「`copy` 接受两个切片作为参数。`dest`（目标）是可变的，而 `source` 不是。」
>
> 「接下来看看健全 Rust 代码的几种形态。」

