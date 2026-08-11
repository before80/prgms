+++
title = "4.4 循环"
date = 2026-08-11T11:30:00+08:00
weight = 28
type = "docs"
description = "循环 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/control-flow-basics/loops.html](https://google.github.io/comprehensive-rust/control-flow-basics/loops.html)

# 4.4 循环

Rust 中有三个循环关键字：`while`、`loop` 和 `for`：

## `while`

[`while` 关键字](https://doc.rust-lang.org/reference/expressions/loop-expr.html#predicate-loops)
的用法与其他语言非常相似：只要条件为真，就执行循环体。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let mut x = 200;
    while x >= 10 {
        x = x / 2;
    }
    dbg!(x);
}
```
