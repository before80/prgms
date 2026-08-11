+++
title = "2.1.5 避免冗余"
date = 2026-08-11T11:30:00+08:00
weight = 395
type = "docs"
description = "05-避免冗余 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/meaningful-doc-comments/avoid-redundancy.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/meaningful-doc-comments/avoid-redundancy.html)

# 2.1.5 避免冗余

名称与类型签名已传达大量信息，不要在注释里再重复一遍！

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
// 重复了名称/类型信息。可省略！
/// Parses an ipv4 from a str. Returns an option for failure modes.
fn parse_ip_addr_v4(input: &str) -> Option<IpAddrV4> { ... }

// 重复了字段名已显而易见的信息。可省略！
struct BusinessAsset {
    /// The customer id.
    customer_id: u64,
}

// 一上来就提类型名，别这样！
/// `ServerSynchronizer` is an orchestrator that sends local edits [...]
struct ServerSynchronizer { ... }

// 更好！聚焦于目的。
/// Sends local edits [...]
struct ServerSynchronizer { ... }

// 一上来就提函数名，别这样！
/// `sync_to_server` sends local edits [...]
fn sync_to_server(...)

// 更好！聚焦于函数本身。
/// Sends local edits [...]
fn sync_to_server(...)
```

> - 动机：仅仅复述名称/签名信息的文档，对 API 用户毫无新意。
>
>   此外，签名信息可能随时间变化，而文档却未同步更新！
>
> - 陷入这种模式是可以理解的！
>
>   对“总是给代码写文档”的天真做法，字面遵循了建议，却未遵循意图。
>
>   有些工具可能强制文档覆盖率，这类文档是容易凑数的“修复”。
>
> - 注意不同文档模式的目的：
>
>   - 库代码需要按用途范围与使用者广度来文档化。
>
>   - 应用代码目的更窄，可以更简单直接。
>
> - 条目的名称是该条目文档的一部分。
>
>   同理，函数的签名是该函数文档的一部分。
>
>   因此：当你开始写文档注释时，条目的某些方面已经被覆盖了！
>
>   不要为了凑条目列表而重复信息。
>
> - 标准库许多地方文档极少，因为名称与类型已给出足够信息。
>
>   经验法则：从用户视角还缺什么信息？除了名称、签名，以及无关的实现细节之外。
>
> - 不要解释 Rust 或标准库的基础知识。假定读者对语言本身有中级理解。聚焦于文档化你的 API。
>
>   例如，若函数返回 `Result`，你不必解释 `Result` 或问号运算符如何工作。
>
> ## 延伸阅读
>
> - `#![warn(missing_docs)]` lint 有助于强制存在文档注释，但会给开发者带来沉重负担，可能导致依赖这些低质量注释模式。
>
>   只有当维护项目的人负担得起其要求时，才应启用此类 lint，且通常仅用于库风格的 crate，而非应用代码。

