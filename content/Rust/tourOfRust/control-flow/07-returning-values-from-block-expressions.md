+++
title = "07-从块表达式返回值"
date = 2026-08-17T22:00:00+08:00
weight = 22
type = "docs"
description = "从块表达式返回值 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/20_zh-cn.html](https://tourofrust.com/20_zh-cn.html)

# 从块表达式返回值

`if`，`match`，函数，以及作用域块都有一种返回值的独特方式。

如果 `if`、`match`、函数或作用域块中的最后一条语句是不带 `;` 的表达式，
Rust 将把它作为一个值从块中返回。这是一种创建简洁逻辑的好方法，它返回一个
可以放入新变量的值。

注意，它还允许 `if` 语句像简洁的三元表达式一样操作。

## 示例代码

```rust
fn example() -> i32 {
    let x = 42;
    // Rust的三元表达式
    let v = if x < 42 { -1 } else { 1 };
    println!("from if: {}", v);

    let food = "hamburger";
    let result = match food {
        "hotdog" => "is hotdog",
        // 注意，当它只是一个返回表达式时，大括号是可选的
        _ => "is not hotdog",
    };
    println!("identifying food: {}", result);

    let v = {
        // 这个作用域块让我们得到一个不影响函数作用域的结果
        let a = 1;
        let b = 2;
        a + b
    };
    println!("from block: {}", v);

    // 在最后从函数中返回值的惯用方法
    v + 4
}

fn main() {
    println!("from function: {}", example());
}
```
