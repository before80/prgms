+++
title = "3.5.4 PhantomData 与类型"
date = 2026-08-11T11:30:00+08:00
weight = 457
type = "docs"
description = "04-PhantomData 与类型 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/borrow-checker-invariants/phantomdata-01-types.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/borrow-checker-invariants/phantomdata-01-types.html)

# 3.5.4 PhantomData 与类型

Newtype 模式有时会与 DRY 原则冲突，我们该如何解决？

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub struct UserId(u64);
impl ChatUser for UserId { /* ... */ }

pub struct PatronId(u64);
impl ChatUser for PatronId { /* ... */ }

pub struct ModeratorId(u64);
impl ChatUser for ModeratorId { /* ... */ }
impl ChatModerator for ModeratorId { /* ... */ }

pub struct AdminId(u64);
impl ChatUser for AdminId { /* ... */ }
impl ChatModerator for AdminId { /* ... */ }
impl ChatAdmin for AdminId { /* ... */ }

// 以此类推 ...
fn main() {}
```
> - 问题：我们想用 newtype 模式区分权限，却不得不为相同数据一遍又一遍地实现相同的 trait。
>
> - 提问：假定各实现细节在类型之间相同，有哪些方法可以避免重复？
>
>   期望：
>   - 做成枚举，而非不同的数据类型。
>   - 将用户 ID 与权限令牌打包，如
>     `struct Admin(u64, UserPermission, ModeratorPermission, AdminPermission);`
>   - 添加编码权限的类型参数。
>   - 提前提到 `PhantomData`（标题里就有）。

