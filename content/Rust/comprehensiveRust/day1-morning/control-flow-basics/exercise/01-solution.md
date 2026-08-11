+++
title = "4.8.1 解答"
date = 2026-08-11T11:30:00+08:00
weight = 36
type = "docs"
description = "01-解答 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/control-flow-basics/solution.html](https://google.github.io/comprehensive-rust/control-flow-basics/solution.html)

# 4.8.1 解答

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 计算从 `n` 开始的 Collatz 序列长度。
fn collatz_length(mut n: i32) -> u32 {
    let mut len = 1;
    while n > 1 {
        n = if n % 2 == 0 { n / 2 } else { 3 * n + 1 };
        len += 1;
    }
    len
}

fn main() {
    println!("Length: {}", collatz_length(11)); // 应为 15
}
```

该解答展示了几个关键的 Rust 特性：

- **`mut` 参数：** 参数 `n` 声明为 `mut n`。这使局部变量 `n` 在函数作用域内可变。它_不会_影响调用方的值，因为整数是按值传递的 `Copy` 类型。
- **`if` 表达式：** Rust 的 `if` 是表达式，意味着它会产生一个值。我们将 `if`/`else` 块的结果直接赋给 `n`。这比在每个分支里分别写 `n = ...` 更简洁。
- **隐式返回：** 函数以 `len`（无分号）结尾，该值会自动返回。

> - 注意：要使 Collatz 序列有效，`n` 必须严格大于 0。函数签名接受 `i32`，但问题描述暗示为正整数。更稳健的实现可能会使用 `u32`，或返回 `Option`/`Result` 来处理无效输入（0 或负数）；若 `n <= 0`，这里可能出现 panic 或无限循环。
> - 若 `n` 变得过大，溢出是潜在问题，与 Fibonacci 练习类似。

