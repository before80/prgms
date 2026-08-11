+++
title = "2.1.7 写什么与为什么，而非怎么与哪里"
date = 2026-08-11T11:30:00+08:00
weight = 397
type = "docs"
description = "07-写什么与为什么，而非怎么与哪里 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/meaningful-doc-comments/what-why-not-how-where.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/meaningful-doc-comments/what-why-not-how-where.html)

# 2.1.7 写什么与为什么，而非怎么与哪里

避免记录可能频繁变更的无关细节。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
// 不好
/// Saves a `User` record to the Postgres database.  
///  
/// This function opens a new connection and begins a transaction. It checks  
/// if a user with the given ID exists with a `SELECT` query. If a user is  
/// not found, performs an `INSERT`.  
///  
/// # Errors  
///  
/// Returns an error if any database operation fails.  
pub fn save_user(user: &User) -> Result<(), db::Error> {
    // ...
}

// 好
/// Atomically saves a user record.  
///  
/// # Errors  
///  
/// Returns a `db::Error::DuplicateUsername` error if the user (keyed by  
/// `user.username` field) already exists.  
pub fn save_user(user: &User) -> Result<(), db::Error> {
    // ...
}
```

> - 动机：用户想知道 API 契约（对该函数保证什么），而非实现细节。
>
> - 动机：解释实现细节的文档注释，比解释契约的注释更快过时。
>
>   内部信息对用户往往无关。想象在函数的文档注释里解释你用 `for` 循环解决问题——这些信息有什么意义？
>
> - 有时确实有必要解释实现，但那多半是因为 API 用户需要知晓其效果或不变量。
>
>   聚焦于那些效果与不变量，而非实现细节本身。
>
>   重申：实现细节可以且将会变化，因此不要解释这些细节。
>
> - 不要谈某物在哪里被使用——这是另一类很快就会过时的信息。

