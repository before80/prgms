+++
title = "2.2.2.5 Hash"
date = 2026-08-11T11:30:00+08:00
weight = 419
type = "docs"
description = "05-Hash — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/hash.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/hash.html)

# 2.2.2.5 Hash

对类型执行哈希。

可派生：✅

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::collections::HashMap;

#[derive(PartialEq, Eq, Hash)]
pub struct User {
    id: u32,
    name: String,
}

fn main() {
    let user = User { id: 1, name: "Alice".into() };
    let mut map = HashMap::new();
    map.insert(user, "value");
}
```

> - 允许类型用于哈希算法，最常与 `HashMap` 等数据结构一起使用。
>
> - 让我们很容易把自定义类型用作 `HashMap` 的键！
>
> - `Hash` 本身不定义任何哈希逻辑，只是把类型的数据送入 `Hasher`。这让我们能在不改变类型 `Hash` 实现的情况下使用不同哈希算法。

