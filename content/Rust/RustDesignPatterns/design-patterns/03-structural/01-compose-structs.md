+++
title = "01-组合结构体"
date = 2026-08-18T22:10:00+08:00
weight = 35
type = "docs"
description = "组合结构体 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/patterns/structural/compose-structs.html](https://rust-unofficial.github.io/patterns/patterns/structural/compose-structs.html)

# 组合结构体

## 描述 {#description}

有时大型结构体会给借用检查器带来问题——虽然字段可以独立借用，但有时整个结构体最终被一次性使用，从而阻止其他用途。一种解决办法是将结构体分解为若干较小的结构体，再将它们组合回原来的结构体。这样每个结构体可以单独借用，并具有更灵活的行为。

这往往也会在其他方面带来更好的设计：应用此设计模式常常会揭示更小的功能单元。

## 示例 {#example}

下面是一个刻意构造的例子，说明借用检查器如何妨碍我们使用结构体：

```rust,ignore
struct Database {
    connection_string: String,
    timeout: u32,
    pool_size: u32,
}

fn print_database(database: &Database) {
    println!("Connection string: {}", database.connection_string);
    println!("Timeout: {}", database.timeout);
    println!("Pool size: {}", database.pool_size);
}

fn main() {
    let mut db = Database {
        connection_string: "initial string".to_string(),
        timeout: 30,
        pool_size: 100,
    };

    let connection_string = &mut db.connection_string;
    print_database(&db);
    *connection_string = "new string".to_string();
}
```

编译器会抛出如下错误：

```ignore
let connection_string = &mut db.connection_string;
                        ------------------------- mutable borrow occurs here
print_database(&db);
               ^^^ immutable borrow occurs here
*connection_string = "new string".to_string();
------------------ mutable borrow later used here
```

我们可以应用此设计模式，将 `Database` 重构为三个较小的结构体，从而解决借用检查问题：

```rust
// Database 现在由三个结构体组合而成——ConnectionString、Timeout 和 PoolSize。
// 让我们把它分解为更小的结构体
#[derive(Debug, Clone)]
struct ConnectionString(String);

#[derive(Debug, Clone, Copy)]
struct Timeout(u32);

#[derive(Debug, Clone, Copy)]
struct PoolSize(u32);

// 然后我们将这些较小的结构体再组合回 `Database`
struct Database {
    connection_string: ConnectionString,
    timeout: Timeout,
    pool_size: PoolSize,
}

// print_database 随后可以接收 ConnectionString、Timeout 和 PoolSize 结构体
fn print_database(connection_str: ConnectionString, timeout: Timeout, pool_size: PoolSize) {
    println!("Connection string: {connection_str:?}");
    println!("Timeout: {timeout:?}");
    println!("Pool size: {pool_size:?}");
}

fn main() {
    // 用这三个结构体初始化 Database
    let mut db = Database {
        connection_string: ConnectionString("localhost".to_string()),
        timeout: Timeout(30),
        pool_size: PoolSize(100),
    };

    let connection_string = &mut db.connection_string;
    print_database(connection_string.clone(), db.timeout, db.pool_size);
    *connection_string = ConnectionString("new string".to_string());
}
```

## 动机 {#motivation}

当你有一个最终包含大量希望独立借用的字段的结构体时，此模式最有用，从而最终获得更灵活的行为。

## 优点 {#advantages}

结构体分解让你可以绕过借用检查器的限制，并且往往能产生更好的设计。

## 缺点 {#disadvantages}

它可能导致代码更冗长。有时，较小的结构体并不是好的抽象，于是我们最终得到更差的设计。那多半是一种“代码异味”，表明程序应当以某种方式重构。

## 讨论 {#discussion}

在没有借用检查器的语言中不需要此模式，因此从这个意义上说它是 Rust 特有的。然而，把功能拆成更小的单元往往会使代码更清晰：这是软件工程中广为认可的原则，与语言无关。

此模式依赖于 Rust 的借用检查器能够彼此独立地借用字段。在示例中，借用检查器知道 `a.b` 与 `a.c` 是不同的，可以独立借用，而不会试图借用整个 `a`——否则此模式就毫无用处。
