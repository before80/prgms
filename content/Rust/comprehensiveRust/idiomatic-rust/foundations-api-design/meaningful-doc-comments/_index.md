+++
title = "2.1 有意义的文档注释"
date = 2026-08-11T11:30:00+08:00
weight = 390
type = "docs"
description = "有意义的文档注释 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/meaningful-doc-comments.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/meaningful-doc-comments.html)

# 2.1 有意义的文档注释

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 客户端的 API // ❌ 缺乏细节
pub mod client {}

/// 从 A 到 B 的函数 // ❌ 冗余
fn a_to_b(a: A) -> B {...}
 
/// 连接到数据库。 // ❌ 缺乏细节
fn connect() -> Result<(), Error> {...}
```

> - 文档注释是开发者最常接触的文档形式。
>
> - 好的文档注释提供代码、名称与类型无法传达的信息，同时不重复那些显而易见的内容。

