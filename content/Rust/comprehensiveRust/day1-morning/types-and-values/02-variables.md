+++
title = "3.2 变量"
date = 2026-08-11T11:30:00+08:00
weight = 18
type = "docs"
description = "02-变量 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/types-and-values/variables.html](https://google.github.io/comprehensive-rust/types-and-values/variables.html)

# 3.2 变量

Rust 通过静态类型提供类型安全。变量绑定使用 `let`：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let x: i32 = 10;
    println!("x: {x}");
    // x = 20;
    // println!("x: {x}");
}
```

> - 取消注释 `x = 20` 以演示变量默认不可变。加上 `mut` 关键字才允许修改。
>
> - 本页启用了警告，例如未使用变量或不必要的 `mut`。多数幻灯片会省略这些，以免警告分散注意力。
>   试着去掉修改但保留 `mut` 关键字。
>
> - 这里的 `i32` 是变量类型。类型必须在编译期已知，但类型推断（稍后介绍）在许多情况下允许省略显式标注。

