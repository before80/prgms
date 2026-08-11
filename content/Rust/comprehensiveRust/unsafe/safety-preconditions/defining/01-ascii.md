+++
title = "4.4.1 示例：ASCII 类型"
date = 2026-08-11T11:30:00+08:00
weight = 524
type = "docs"
description = "01-示例：ASCII 类型 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/safety-preconditions/ascii.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/safety-preconditions/ascii.html)

# 4.4.1 示例：ASCII 类型

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 保证以 7 位 ASCII 编码的文本。
pub struct Ascii<'a>(&'a mut [u8]);

impl<'a> Ascii<'a> {
    pub fn new(bytes: &'a mut [u8]) -> Option<Self> {
        bytes.iter().all(|&b| b.is_ascii()).then(|| Ascii(bytes))
    }

    /// 从不检查 ASCII 有效性的字节切片创建新的 `Ascii`。
    ///
    /// # 安全
    ///
    /// 提供非 ASCII 字节会导致未定义行为。
    pub unsafe fn new_unchecked(bytes: &'a mut [u8]) -> Self {
        Ascii(bytes)
    }
}
```

> 「`Ascii` 类型是对字节切片的极简包装。内部表示相同。但 `Ascii` 要求最高位不能置位。」
>
> 可选：扩展示例，说明可以在测试中使用 `debug_assert!` 检查前置条件，而不影响 release 构建。
>
> ```rust
> // Copyright 2026 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> unsafe fn new_unchecked(bytes: &mut [u8]) -> Self {
>     debug_assert!(bytes.iter().all(|&b| b.is_ascii()))
>     Ascii(bytes)
> }
> ```

