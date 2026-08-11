+++
title = "3.6 Unsafe Trait"
date = 2026-08-11T11:30:00+08:00
weight = 205
type = "docs"
description = "05-Unsafe Trait — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-rust/unsafe-traits.html](https://google.github.io/comprehensive-rust/unsafe-rust/unsafe-traits.html)

# 3.6 Unsafe Trait

与函数类似，若实现方必须保证特定条件才能避免未定义行为，可以把 trait 标记为 `unsafe`。

例如，`zerocopy` crate 有一个 unsafe trait，大致
[如下](https://docs.rs/zerocopy/latest/zerocopy/trait.IntoBytes.html)：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::{mem, slice};

/// ...
/// # Safety
/// 该类型必须有确定的表示形式，且没有填充字节（padding）。
pub unsafe trait IntoBytes {
    fn as_bytes(&self) -> &[u8] {
        let len = mem::size_of_val(self);
        let slf: *const Self = self;
        unsafe { slice::from_raw_parts(slf.cast::<u8>(), len) }
    }
}

// SAFETY: `u32` 有确定的表示形式，且没有填充字节。
unsafe impl IntoBytes for u32 {}
```

> <summary>讲师备注</summary>
>
> trait 的 Rustdoc 中应有 `# Safety` 小节，说明安全实现该 trait 的要求。
>
> `IntoBytes` 实际的 safety 小节更长、更复杂。
>
> 内置的 `Send` 和 `Sync` trait 是 unsafe 的。

