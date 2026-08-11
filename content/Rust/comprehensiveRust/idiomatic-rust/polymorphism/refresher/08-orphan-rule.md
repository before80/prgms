+++
title = "4.1.8 孤儿规则"
date = 2026-08-11T11:30:00+08:00
weight = 477
type = "docs"
description = "08-孤儿规则 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/orphan-rule.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/orphan-rule.html)

# 4.1.8 孤儿规则

是什么阻止用户为任意类型编写任意 trait 实现？

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
// crate `postgresql-bindings`

pub struct PostgresqlConn(/* details */);

// crate `database-traits`，依赖 `postgresql-bindings`

pub trait DbConnection {
    /* methods */
}

impl DbConnection for PostgresqlConn {} // ✅，`DbConnection` 是本地的。

// crate `mycoolnewdb` 依赖 `database-traits`

pub struct MyCoolNewDbConn(/* details */);

impl DbConnection for MyCoolNewDbConn {} // ✅，`MyCoolNewDbConn` 是本地的。

// `PostgresqlConn` 与 `DbConnection` 对 `mycoolnewdb` 都不是本地的。
// 这会导致 PostgresqlConn 上出现两份 `DbConnection` 实现！
impl DbConnection for PostgresqlConn {} // ❌🔨
```

> - Rust 的 trait 在整个生态中绝不应该被实现两次。同一 trait 对同一类型的两份实现是无法解决的冲突。
>
> - 在单个 crate 内，我们可以检测多重定义并禁止；但整个 Rust 生态中的各个 crate 之间呢？
>
> - 类型要么对某个 crate 是 *本地的*（在该处定义），要么不是。
>
>   示例「crate」中，`PostgresqlConn` 本地于 `postgresql-bindings`，`MyCoolNewDbConn` 本地于 `mycoolnewdb`。
>
> - Trait 同样要么对某个 crate 是 *本地的*（在该处定义），要么不是。
>
>   同样在示例中，`DbConnection` trait 本地于 `database-traits`。
>
> - 只要有一方是本地的，就可以编写 trait 实现。
>
>   若 trait 是本地的，你可以为任意类型编写该 trait 的实现。
>
>   若类型是本地的，你可以为该类型编写任意 trait 的实现。
>
> - 超出这些边界，就不能再写 trait 实现。
>
>   这保证了实现的「一致性」（coherence）：跨 crate 时，某一类型对某一 trait 只能有一份实现。
>
> 参考：
>
> - https://doc.rust-lang.org/stable/reference/items/implementations.html#r-items.impl.trait.orphan-rule

