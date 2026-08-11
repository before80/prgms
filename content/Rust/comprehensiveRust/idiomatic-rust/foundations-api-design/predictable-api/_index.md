+++
title = "2.2 可预测的 API"
date = 2026-08-11T11:30:00+08:00
weight = 399
type = "docs"
description = "可预测的 API — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api.html)

# 2.2 可预测的 API

通过命名约定与实现常见 trait，让你的 API 可预测。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
/* 这个类型应该实现哪些 trait？ */
pub struct ApiToken(String);

impl ApiToken {
    // 这个方法应该叫什么？
    pub unsafe fn ____(String) -> ApiToken;
}
```

> - 可预测的 API 是指：用户能根据名称、类型与签名等表层细节，对 API 某部分做出合理假设。
>
> - 我们将审视 Rust 中常见的命名约定——它们让用户能快速搜索符合需求的方法，并快速理解现有代码。
>
> - 我们还将审视类型常实现的常见 trait，以及何时为你定义的类型实现它们。

