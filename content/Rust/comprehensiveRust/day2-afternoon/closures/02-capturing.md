+++
title = "2.2 捕获"
date = 2026-08-11T11:30:00+08:00
weight = 98
type = "docs"
description = "02-捕获 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/closures/capturing.html](https://google.github.io/comprehensive-rust/closures/capturing.html)

# 2.2 捕获

闭包可以从定义它的环境中捕获变量。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let max_value = 5;
    let clamp = |v| {
        if v > max_value { max_value } else { v }
    };

    dbg!(clamp(1));
    dbg!(clamp(3));
    dbg!(clamp(5));
    dbg!(clamp(7));
    dbg!(clamp(10));
}
```

> - 默认情况下，闭包按引用捕获值。这里 `max_value` 被 `clamp` 捕获，但仍可供 `main` 打印。试着把 `max_value` 改成可变的、修改它，再打印 clamp 后的值。为什么不行？
>
> - 若闭包会修改值，它会按可变引用捕获。试着在 `clamp` 里加 `max_value += 1`。
>
> - 可以用 `move` 关键字强制闭包移动值而不是引用它们。这有助于处理生命周期，例如闭包必须比被捕获的值活得更久时（生命周期后面会讲）。
>
>   写法形如 `move |v| ..`。试着加上这个关键字，看看定义 `clamp` 之后 `main` 是否还能访问 `max_value`。
>
> - 默认情况下，闭包会以尽可能「要求最少」的方式捕获外层作用域中的每个变量（能共享引用就共享引用，然后是独占引用，最后才是移动）。`move` 关键字强制按值捕获。

