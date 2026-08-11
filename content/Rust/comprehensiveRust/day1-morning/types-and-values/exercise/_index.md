+++
title = "3.6 练习：斐波那契"
date = 2026-08-11T11:30:00+08:00
weight = 22
type = "docs"
description = "练习：斐波那契 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/types-and-values/exercise.html](https://google.github.io/comprehensive-rust/types-and-values/exercise.html)

# 3.6 练习：斐波那契

斐波那契数列以 `[0, 1]` 开始。对于 `n > 1`，下一项是前两项之和。

编写函数 `fib(n)`，计算第 n 个斐波那契数。这个函数何时会 panic？

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn fib(n: u32) -> u32 {
    if n < 2 {
        // 基本情况。
        return todo!("Implement this");
    } else {
        // 递归情况。
        return todo!("Implement this");
    }
}

fn main() {
    let n = 20;
    println!("fib({n}) = {}", fib(n));
}
```

> - 这是经典的递归入门练习。
> - 鼓励学员思考基本情况与递归步骤。
> - “这个函数何时会 panic？”是在提示思考整数溢出。斐波那契数列增长很快！
> - 学员也可能想出迭代解法，这是讨论递归与迭代权衡的好机会（例如性能、深层递归的栈溢出）。

