+++
title = "02-loop 循环"
date = 2026-08-20T21:20:00+08:00
weight = 38
type = "docs"
description = "loop 循环 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/flow_control/loop.html](https://doc.rust-lang.org/stable/rust-by-example/flow_control/loop.html)

# loop 循环

Rust 提供了 `loop` 关键字来表示一个无限循环。

可以使用 `break` 语句在任何时候退出一个循环，还可以使用 `continue` 跳过循环体的剩余部分并开始下一轮循环。

```rust
fn main() {
    let mut count = 0u32;

    println!("Let's count until infinity!");

    // 无限循环
    loop {
        count += 1;

        if count == 3 {
            println!("three");

            // 跳过这次迭代的剩下内容
            continue;
        }

        println!("{}", count);

        if count == 5 {
            println!("OK, that's enough");

            // 退出循环
            break;
        }
    }
}
```
