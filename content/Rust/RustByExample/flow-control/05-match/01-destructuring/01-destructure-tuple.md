+++
title = "01-元组"
date = 2026-08-20T21:20:00+08:00
weight = 45
type = "docs"
description = "元组 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/flow_control/match/destructuring/destructure_tuple.html](https://doc.rust-lang.org/stable/rust-by-example/flow_control/match/destructuring/destructure_tuple.html)

# 元组

元组可以在 `match` 中解构，如下所示：

```rust
fn main() {
    let triple = (0, -2, 3);
    // 试一试 ^ 将不同的值赋给 `triple`

    println!("Tell me about {:?}", triple);
    // match 可以解构一个元组
    match triple {
        // 解构出第二个和第三个元素
        (0, y, z) => println!("First is `0`, `y` is {:?}, and `z` is {:?}", y, z),
        (1, ..)  => println!("First is `1` and the rest doesn't matter"),
        // `..` 可用来忽略元组的其余部分
        _      => println!("It doesn't matter what they are"),
        // `_` 表示不将值绑定到变量
    }
}
```
### 参见： {#参见}

[元组](../../../primitives/02-tuples/)
