+++
title = "2.1.6 名称与签名不够"
date = 2026-08-11T11:30:00+08:00
weight = 396
type = "docs"
description = "06-名称与签名不够 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/meaningful-doc-comments/what-isnt-docs.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/meaningful-doc-comments/what-isnt-docs.html)

# 2.1.6 名称与签名不够

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
// 不好
/// Returns a future that resolves when operation completes.  
fn sync_to_server() -> Future<Bool>;

// 好
/// Sends local edits to the server, overwriting concurrent edits  
/// if any happened.  
fn sync_to_server() -> Future<Bool>;

// 不好
/// Returns an error if sending the email fails.  
fn send(&self, email: Email) -> Result<(), Error>;

// 好
/// Queues the email for background delivery and returns immediately.  
///
/// Returns an error immediately if the email is malformed.  
fn send(&self, email: Email) -> Result<(), Error>;
```

> - 动机：API 设计者可能过度相信“函数名与签名就够当文档”。
>
> - 再次强调：名称与类型是文档的*一部分*。它们并不总是全部故事！
>
> - 考虑名称、参数名或签名未覆盖的函数行为。
>
>   - 并不显然 `sync_to_server()` 可能覆盖某些东西（导致数据丢失），因此要文档化。
>
>   - 在邮件示例中，并不显然函数可以返回成功，却仍未能投递邮件。
>
> - 用注释消除歧义。细微行为、API 用户可能踩坑的行为，应当文档化。

