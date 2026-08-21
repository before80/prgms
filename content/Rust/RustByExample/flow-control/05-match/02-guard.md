+++
title = "02-卫语句"
date = 2026-08-20T21:20:00+08:00
weight = 50
type = "docs"
description = "卫语句 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/flow_control/match/guard.html](https://doc.rust-lang.org/stable/rust-by-example/flow_control/match/guard.html)

# 卫语句

可以加上 `match` **卫语句**（guard） 来过滤分支。

```rust
fn main() {
    let pair = (2, -2);
    // 试一试 ^ 将不同的值赋给 `pair`

    println!("Tell me about {:?}", pair);
    match pair {
        (x, y) if x == y => println!("These are twins"),
        // ^ `if` 条件部分是一个卫语句
        (x, y) if x + y == 0 => println!("Antimatter, kaboom!"),
        (x, _) if x % 2 == 1 => println!("The first one is odd"),
        _ => println!("No correlation..."),
    }
}
```
### 参见： {#参见}

[元组](../../primitives/02-tuples/)
