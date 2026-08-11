+++
title = "4.1 块与作用域"
date = 2026-08-11T11:30:00+08:00
weight = 25
type = "docs"
description = "01-块与作用域 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/control-flow-basics/blocks-and-scopes.html](https://google.github.io/comprehensive-rust/control-flow-basics/blocks-and-scopes.html)

# 4.1 块与作用域

- Rust 中的块（block）是由花括号 `{}` 括起的一系列表达式。
- 块中最后一个表达式决定整个块的值和类型。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let z = 13;
    let x = {
        let y = 10;
        dbg!(y);
        z - y
    };
    dbg!(x);
    // dbg!(y);
}
```

如果最后一个表达式以 `;` 结尾，则结果值和类型为 `()`。

变量的作用域仅限于包围它的块。

> - 可以说明 `dbg!` 是一个 Rust 宏，用于打印并返回给定表达式的值，便于临时调试。
>
> - 可以演示修改块中最后一行如何改变块的值。例如，添加/删除分号，或使用 `return`。
>
> - 演示在作用域外访问 `y` 将无法编译。
>
> - 值在离开作用域时实际上会被“释放”，即便它们在栈上的数据可能仍然存在。

