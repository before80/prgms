+++
title = "3.4.3 实现 unsafe trait"
date = 2026-08-11T11:30:00+08:00
weight = 507
type = "docs"
description = "03-实现 unsafe trait — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/warm-up/unsafe-impl.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/warm-up/unsafe-impl.html)

# 3.4.3 实现 unsafe trait

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub struct LogicalClock {
    inner: std::sync::Arc<std::sync::atomic::AtomicUsize>,
}

// ...

impl Send for LogicalClock {}
impl Sync for LogicalClock {}
```

> 「在看代码之前，我们应再次确认大家都了解 trait 是什么。有人能为全班解释 trait 吗？
>
> - 「trait 常被描述为创建共享行为的方式。将 trait 视为共享行为，侧重于方法的语法与签名。
> - 「还有更深层的理解：trait 是一组要求。这强调实现类型之间的共享语义。」
>
> 「有人能解释 `Send` 和 `Sync` trait 是什么吗？
>
> - 若无人回答
>   - 「`Send` 和 `Sync` 与并发相关。细节很多，但广义而言，`Send` 类型可以按值在线程间共享。`Sync` 类型必须按引用共享。
>   - 要确保跨线程边界共享数据是安全的，需要遵循许多规则。编译器无法检查这些规则，因此代码作者必须承担维护它们的责任。
>   - `Arc` 实现了 `Send` 和 `Sync`，因此我们的时钟也可以安全地实现它们。
>   - 指出 _atomic_ 一词来自古希腊语，意为「不可分割的」或「整体的」，而非当代英语中「微小粒子」的含义，可能也有帮助。」

