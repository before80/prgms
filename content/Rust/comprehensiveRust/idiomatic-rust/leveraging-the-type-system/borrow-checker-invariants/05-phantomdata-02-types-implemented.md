+++
title = "3.5.5 PhantomData 与类型（实现）"
date = 2026-08-11T11:30:00+08:00
weight = 458
type = "docs"
description = "05-PhantomData 与类型（实现） — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/borrow-checker-invariants/phantomdata-02-types-implemented.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/borrow-checker-invariants/phantomdata-02-types-implemented.html)

# 3.5.5 PhantomData 与类型（实现）

通过添加类型参数来解决上一页的问题。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
// use std::marker::PhantomData;

pub struct ChatId<T> { id: u64, tag: T }

pub struct UserTag;
pub struct AdminTag;

pub trait ChatUser {/* ... */}
pub trait ChatAdmin {/* ... */}

impl ChatUser for UserTag {/* ... */}
impl ChatUser for AdminTag {/* ... */} // 管理员也是用户
impl ChatAdmin for AdminTag {/* ... */}

// impl <T> Debug for UserTag<T> {/* ... */}
// impl <T> PartialEq for UserTag<T> {/* ... */}
// impl <T> Eq for UserTag<T> {/* ... */}
// 以此类推 ...

impl <T: ChatUser> ChatId<T> {/* 用户及以上的全部功能 */}
impl <T: ChatAdmin> ChatId<T> {/* 仅管理员的全部功能 */}

fn main() {}
```
> - 这里我们使用类型参数，并将权限关在实现不同权限 trait 的「标签」类型后面。
>
>   标签类型（或标记类型）是零大小类型，对用户与 API 设计者有某种语义含义。
>
> - 提问：让它成为该类型的实际实例会带来什么问题？
>
>   答：若它不是零大小类型（如 `()` 或 `struct MyTag;`），那么当我们只关心仅在编译期相关的类型信息时，会分配比需要更多的内存。
>
> - 演示：完全去掉 `tag` 值，然后编译！
>
>   这不会编译，因为有一个未使用的（phantom）类型参数。
>
>   这正是 `PhantomData` 出场之处！
>
> - 演示：取消注释 `PhantomData` 导入，并将 `ChatId<T>` 改为如下：
>
>   ```rust
>   // Copyright 2025 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   pub struct ChatId<T> {
>       id: u64,
>       tag: PhantomData<T>,
>   }
>   ```
>
> - `PhantomData<T>` 是带类型参数的零大小类型。我们可以像其他 ZST 一样构造它的值：
>   `let phantom: PhantomData<UserTag> = PhantomData;`，或使用
>   `PhantomData::default()` 实现。
>
>   演示：为 `ChatId<T>` 实现 `From<u64>`，强调 `PhantomData` 的构造
>
>   ```rust
>   // Copyright 2025 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   impl<T> From<u64> for ChatId<T> {
>       fn from(value: u64) -> Self {
>           ChatId {
>               id: value,
>               // 或 `PhantomData::default()`
>               tag: PhantomData,
>           }
>       }
>   }
>   ```
>
> - `PhantomData` 可作为 Typestate 模式的一部分，使数据具有相同结构但不同方法，例如让 `TaggedData<Start>` 实现 `TaggedData<End>` 没有的方法或 trait 实现。

