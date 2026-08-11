+++
title = "4.7 宏"
date = 2026-08-11T11:30:00+08:00
weight = 34
type = "docs"
description = "05-宏 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/control-flow-basics/macros.html](https://google.github.io/comprehensive-rust/control-flow-basics/macros.html)

# 4.7 宏

宏在编译期间展开为 Rust 代码，可以接受可变数量的参数。它们以末尾的 `!` 区分。Rust 标准库提供了一系列有用的宏。

- `println!(format, ..)` 向标准输出打印一行，并应用 [`std::fmt`](https://doc.rust-lang.org/std/fmt/index.html) 中描述的格式化。
- `format!(format, ..)` 与 `println!` 类似，但把结果作为字符串返回。
- `dbg!(expression)` 记录表达式的值并返回它。
- `todo!()` 标记某段代码尚未实现。若执行到这里，会 panic。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn factorial(n: u32) -> u32 {
    let mut product = 1;
    for i in 1..=n {
        product *= dbg!(i);
    }
    product
}

fn fizzbuzz(n: u32) -> u32 {
    todo!()
}

fn main() {
    let n = 4;
    println!("{n}! = {}", factorial(n));
}
```

> 本节要带走的是：这些常用便利工具存在，以及如何使用它们。它们为何定义为宏、展开成什么，并不是特别关键。
>
> 本课程不涵盖如何定义宏，但后续章节会介绍 derive 宏的用法。
>
> ## 扩展阅读
>
> 标准库还提供许多其他有用的宏。若学员想了解更多，可以分享以下例子：
>
> - [`assert!`] 及相关宏可用于在代码中添加断言。它们在编写测试时被大量使用。
> - [`unreachable!`] 用于标记理论上永远不会走到的控制流分支。
> - [`eprintln!`] 允许你向 stderr 打印。


[`assert!`]: https://doc.rust-lang.org/stable/std/macro.assert.html
[`unreachable!`]: https://doc.rust-lang.org/stable/std/macro.unreachable.html
[`eprintln!`]: https://doc.rust-lang.org/stable/std/macro.eprintln.html
