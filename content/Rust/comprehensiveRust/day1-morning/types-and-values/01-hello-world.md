+++
title = "3.1 你好，世界"
date = 2026-08-11T11:30:00+08:00
weight = 17
type = "docs"
description = "01-你好，世界 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/types-and-values/hello-world.html](https://google.github.io/comprehensive-rust/types-and-values/hello-world.html)

# 3.1 你好，世界

让我们从最简单的 Rust 程序开始——经典的 Hello World：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    println!("Hello 🌍!");
}
```

你可以看到：

- 函数用 `fn` 引入。
- `main` 函数是程序入口。
- 代码块用花括号分隔，与 C/C++ 类似。
- 语句以 `;` 结尾。
- `println` 是宏，调用时用 `!` 标明。
- Rust 字符串为 UTF-8 编码，可包含任意 Unicode 字符。

> 本页旨在让学员对 Rust 代码感到熟悉。接下来四天他们会看到大量代码，所以我们从小而熟悉的例子起步。
>
> 要点：
>
> - Rust 很像 C/C++/Java 传统中的其他语言。它是命令式的，除非绝对必要，否则不会去重新发明轮子。
>
> - Rust 是现代语言，完整支持 Unicode。
>
> - 当你需要可变数量参数时，Rust 使用宏（没有函数
>   [重载](../control-flow-basics/functions.md)）。
>
> - `println!` 之所以是宏，是因为它需要根据格式字符串处理任意数量的参数，普通函数做不到。
>   除此以外，可以像普通函数一样对待它。
>
> - Rust 是多范式的。例如，它有强大的
>   [面向对象特性](https://doc.rust-lang.org/book/ch17-00-oop.html)，
>   虽不是函数式语言，但也包含一系列
>   [函数式概念](https://doc.rust-lang.org/book/ch13-00-functional-features.html)。

