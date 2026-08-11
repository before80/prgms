+++
title = "2.2.2.10 Serialize 与 Deserialize"
date = 2026-08-11T11:30:00+08:00
weight = 424
type = "docs"
description = "10-Serialize 与 Deserialize — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/serde.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/serde.html)

# 2.2.2.10 Serialize 与 Deserialize

像 `serde` 这样的 crate 可自动实现序列化。

可派生：✅

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Serialize, Deserialize)]
struct ExtraData {
    fav_color: String,
    name_of_dog: String,
}

#[derive(Serialize, Deserialize)]
struct Data {
    name: String,
    age: usize,
    extra_data: ExtraData,
}
```

> - 为类型提供序列化与反序列化功能，使 Rust 数据类型可与 JSON 等数据格式互相转换。
>
> - 标准库没有内置序列化功能，但 serde crate 是社区做序列化的标准接口。
>
> - 何时不要实现：若类型包含不应被错误地保存到磁盘或通过网络发送的敏感数据，考虑不为该类型实现 Serialize/Deserialize。
>
>   与 `Debug` 有相同安全顾虑，但鉴于序列化常用于网络，风险可能更高。

