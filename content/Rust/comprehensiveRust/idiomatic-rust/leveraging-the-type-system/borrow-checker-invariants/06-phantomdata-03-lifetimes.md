+++
title = "3.5.6 PhantomData：外部资源的生命周期"
date = 2026-08-11T11:30:00+08:00
weight = 459
type = "docs"
description = "06-PhantomData：外部资源的生命周期 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/borrow-checker-invariants/phantomdata-03-lifetimes.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/borrow-checker-invariants/phantomdata-03-lifetimes.html)

# 3.5.6 PhantomData：外部资源的生命周期

外部资源的不变量常常与我们能用生命周期规则做的事相匹配。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
// use std::marker::PhantomData;

/// 直接到 C 中数据库库的 FFI。
/// 我们得到的就是这样的 API，无法对其施加影响。
mod ffi {
    pub type DatabaseHandle = u8; // 同时最多打开 255 个数据库

    fn database_open(name: *const std::os::raw::c_char) -> DatabaseHandle {
        unimplemented!()
    }
    // ... 等等。
}

struct DatabaseConnection(ffi::DatabaseHandle);

struct Transaction<'a>(&'a mut DatabaseConnection);

impl DatabaseConnection {
    fn new_transaction(&mut self) -> Transaction<'_> {
        Transaction(self)
    }
}

fn main() {}
```

> - 回想
>   [别名 XOR 可变](./03-aliasing-xor-mutability.md)
>   示例中的事务 API。
>
>   我们在事务类型中持有对数据库连接的可变引用，以便在事务活动时锁定数据库。
>
>   本例中，我们想在外部的、非 Rust API 之上实现 `Transaction` API。
>
>   我们从定义持有 `&mut DatabaseConnection` 的 `Transaction` 类型开始。
>
> - 提问：此实现的局限是什么？假定 `u8` 在实现上准确，且对我们使用外部 API 有足够信息。
>
>   期望：
>   - 在 64 位平台上，间接层比我们需要的多占 7 字节，并在运行时付出指针解引用的代价。
>
> - 问题：我们希望事务借用创建它的数据库连接，但不希望 `Transaction` 对象存储真正的引用。
>
> - 提问：当我们去掉 `Transaction` 中的可变引用但保留生命周期参数时会发生什么？
>
>   期望：未使用的生命周期参数！
>
> - 与先前幻灯片中的类型标签类似，我们可以引入 `PhantomData` 来为我们捕获这个未使用的生命周期参数。
>
>   区别在于我们需要将生命周期与另一类型一起使用，但那另一类型不太重要。
>
> - 演示：将 `Transaction` 改为如下：
>
>   ```rust
>   // Copyright 2025 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   struct Transaction<'a> {
>       connection: DatabaseConnection,
>       _phantom: PhantomData<&'a mut DatabaseConnection>,
>   }
>   ```
>
>   更新 `DatabaseConnection::new_transaction()` 方法：
>
>   ```rust
>   // Copyright 2025 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   impl DatabaseConnection {
>       fn new_transaction<'a>(&'a mut self) -> Transaction<'a> {
>           Transaction { connection: DatabaseConnection(self.0), _phantom: PhantomData }
>       }
>   }
>   ```
>
>   这给出一个拥有的数据库连接，它与创建它的 `DatabaseConnection` 绑定，但运行时内存占用小于存储引用的版本。
>
>   因为 `PhantomData` 是零大小类型（如 `()` 或 `struct MyZeroSizedType;`），`Transaction` 的大小现在与 `u8` 相同。
>
>   持有引用的实现则与 `usize` 一样大。
>
> ## 深入探索
>
> - 这种在类型与值之间编码关系的方式，与 unsafe 结合时非常强大，因为可操纵生命周期的方式几乎变得任意。这也很危险，但与外部、机械验证的证明等工具结合时，我们可以安全地编码循环/自引用类型，同时在相关数据类型中编码生命周期与安全期望。
>
> - [GhostCell (2021)](https://plv.mpi-sws.org/rustbelt/ghostcell/) 论文及其
>   [相关实现](https://gitlab.mpi-sws.org/FP/ghostcell)
>   展示了这类工作。尽管借用检查器有限制，仍有办法使用逃生舱，然后**证明你使用这些逃生舱的方式是一致且安全的**。

