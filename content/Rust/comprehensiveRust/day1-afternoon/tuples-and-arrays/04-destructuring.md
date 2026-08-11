+++
title = "2.4 模式与解构"
date = 2026-08-11T11:30:00+08:00
weight = 43
type = "docs"
description = "04-模式与解构 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/tuples-and-arrays/destructuring.html](https://google.github.io/comprehensive-rust/tuples-and-arrays/destructuring.html)

# 2.4 模式与解构

Rust 支持用模式匹配把元组这类较大的值解构为各个组成部分：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn check_order(tuple: (i32, i32, i32)) -> bool {
    let (left, middle, right) = tuple;
    left < middle && middle < right
}

fn main() {
    let tuple = (1, 5, 3);
    println!(
        "{tuple:?}: {}",
        if check_order(tuple) { "ordered" } else { "unordered" }
    );
}
```

> - 这里用到的模式是“不可失败的”（irrefutable），意味着编译器能静态验证 `=` 右侧值的结构与模式一致。
> - 变量名本身就是总能匹配任意值的不可失败模式，因此也可以用 `let` 声明单个变量。
> - Rust 还支持在条件中使用模式，从而同时完成相等比较与解构。这种模式匹配稍后会更详细讨论。
> - 修改上面的例子，观察当模式与被匹配的值不匹配时编译器给出的错误。

