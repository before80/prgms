+++
title = "2.2.2 实现常见 Trait"
date = 2026-08-11T11:30:00+08:00
weight = 414
type = "docs"
description = "实现常见 Trait — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits.html)

# 2.2.2 实现常见 Trait

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug, PartialEq, Eq, PartialOrd, Ord, Hash, Clone /* ... */)]
pub struct MyData {
    pub name: String,
    pub number: usize,
    pub data: [u8; 64],
}
```

> - Trait 是 Rust 语言最强大的工具之一。语言与生态期望你使用它们，因此*可预测性*很大一部分就在于类型实现了哪些 trait！
>
> - 你应在自己撰写的类型上慷慨地实现 trait，但也有注意事项！
>
> - 记住，许多 trait 可以*派生*（derive）：由编译器插件（宏）为你编写实现！
>
> - 生态 trait（如 De/Serialize）的作者为用户提供了 derive 实现，使得实现这类 trait 对开发者而言几乎无需投入！

