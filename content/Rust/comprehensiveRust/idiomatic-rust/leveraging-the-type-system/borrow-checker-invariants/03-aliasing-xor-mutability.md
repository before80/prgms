+++
title = "3.5.3 互斥引用 / 「别名 XOR 可变」"
date = 2026-08-11T11:30:00+08:00
weight = 456
type = "docs"
description = "03-互斥引用 / 「别名 XOR 可变」 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/borrow-checker-invariants/aliasing-xor-mutability.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/borrow-checker-invariants/aliasing-xor-mutability.html)

# 3.5.3 互斥引用 / 「别名 XOR 可变」

我们可以利用 `&T` 与 `&mut T` 引用的互斥性，防止数据在就绪前被使用。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub struct QueryResult;
pub struct DatabaseConnection {/* fields omitted */}

impl DatabaseConnection {
    pub fn new() -> Self {
        Self {}
    }
    pub fn results(&self) -> &[QueryResult] {
        &[] // 伪造结果
    }
}

pub struct Transaction<'a> {
    connection: &'a mut DatabaseConnection,
}

impl<'a> Transaction<'a> {
    pub fn new(connection: &'a mut DatabaseConnection) -> Self {
        Self { connection }
    }
    pub fn query(&mut self, _query: &str) {
        // 发送查询，但不等待结果。
    }
    pub fn commit(self) {
        // 完成执行事务并取回结果。
    }
}

fn main() {
    let mut db = DatabaseConnection::new();

    // 事务 `tx` 可变地借用 `db`。
    let mut tx = Transaction::new(&mut db);
    tx.query("SELECT * FROM users");

    // 这不会编译，因为 `db` 已被 `tx` 可变借用。
    // let results = db.results(); // ❌🔨

    // 对 `db` 的借用在 `tx` 被 `commit()` 消费时结束。
    tx.commit();

    // 现在可以再次借用 `db`。
    let results = db.results();
}
```

> - 动机：在此数据库 API 中，查询被启动以异步执行，结果仅在整个事务完成后才可用。
>
>   用户可能认为查询会立即执行，并在结果可用之前尝试读取。这种 API 误用可能使应用读到不完整或不正确的数据。
>
>   尽管是明显的误解，这类情况在实践中仍可能发生。
>
>   提问：有没有人因未阅读正确用法文档而误解过 API？
>
>   期望：职业生涯早期或大学期间的错误与误解示例。
>
>   随着 API 规模与用户基数增长，对 API 所代表系统有深入了解的用户比例会变小。
>
> - 本例展示我们如何用「别名 XOR 可变」（Aliasing XOR Mutability）防止这类误用。
>
> - 若程序员假定查询立即执行而非被启动以异步执行，代码可能在结果就绪前读取它们。
>
> - `Transaction` 类型的构造函数接受对数据库连接的可变引用，并将其存入返回的 `Transaction` 值。
>
>   这里的显式生命周期不必吓人，它只是表示「本例中，`Transaction` 的生命周期短于传给它的 `DatabaseConnection`」。
>
>   引用是可变的，以便完全锁定 `DatabaseConnection`，使其不能被其他用途使用，例如开始更多事务或读取结果。
>
> - 当 `Transaction` 存在时，我们不能触碰创建它时的那个 `DatabaseConnection` 变量。
>
>   演示：取消注释 `db.results()` 行。这样做会导致编译错误，因为 `db` 已被可变借用。
>
> - 注意：查询结果不是公开的，而是放在 getter 函数后面，这让我们能强制不变量「用户只能在没有活动事务时查看查询结果」。
>
>   若查询结果放在公开结构体字段中，该不变量可能被破坏。

