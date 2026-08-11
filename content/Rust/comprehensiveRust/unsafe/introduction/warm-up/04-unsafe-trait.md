+++
title = "3.4.4 定义 unsafe trait"
date = 2026-08-11T11:30:00+08:00
weight = 508
type = "docs"
description = "04-定义 unsafe trait — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/warm-up/unsafe-trait.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/warm-up/unsafe-trait.html)

# 3.4.4 定义 unsafe trait

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 表示该类型使用 32 位内存。
pub trait Size32 {}
```

> 「现在我们来定义自己的 unsafe trait。」
>
> 添加 `unsafe` 关键字并编译代码。
>
> 「若 trait 的要求是语义层面的，你的 trait 可能根本不需要任何方法。然而，文档是必不可少的。」
>
> 「没有方法的 trait 称为 marker trait（标记 trait）。为类型实现它们时，你是在向类型系统添加信息。你现在让编译器能够讨论满足文档中所述要求的类型。」

