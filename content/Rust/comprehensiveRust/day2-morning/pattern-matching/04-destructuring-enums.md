+++
title = "2.4 解构枚举"
date = 2026-08-11T11:30:00+08:00
weight = 69
type = "docs"
description = "04-解构枚举 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/pattern-matching/destructuring-enums.html](https://google.github.io/comprehensive-rust/pattern-matching/destructuring-enums.html)

# 2.4 解构枚举

与元组一样，枚举也可以通过匹配来解构：

模式还可以把变量绑定到值的各个部分。这就是检查类型结构的方式。先从一个简单的 `enum` 开始：

```rust
// Copyright 2022 Google LLC
// SPDX-License-Identifier: Apache-2.0
enum Result {
    Ok(i32),
    Err(String),
}

fn divide_in_two(n: i32) -> Result {
    if n % 2 == 0 {
        Result::Ok(n / 2)
    } else {
        Result::Err(format!("cannot divide {n} into two equal parts"))
    }
}

fn main() {
    let n = 100;
    match divide_in_two(n) {
        Result::Ok(half) => println!("{n} divided in two is {half}"),
        Result::Err(msg) => println!("sorry, an error happened: {msg}"),
    }
}
```

这里我们用匹配分支_解构_了 `Result` 值。第一个分支中，`half` 绑定到 `Ok` 变体内的值；第二个分支中，`msg` 绑定到错误信息。

> - `if`/`else` 表达式返回一个枚举，随后用 `match` 拆开。
> - 可以试着给枚举定义增加第三个变体，并运行代码查看报错。指出哪些地方变得不完备（inexhaustive），以及编译器如何给出提示。
> - 枚举变体中的值只有在模式匹配之后才能访问。
> - 演示匹配不完备时会发生什么。指出 Rust 编译器在确认所有情况都已处理时的优势。
> - 给枚举定义增加一个结构体风格的变体，并在 `match` 中演示其语法。指出这在语法上与匹配结构体很相似。

