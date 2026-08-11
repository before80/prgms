+++
title = "3.6.1 解答"
date = 2026-08-11T11:30:00+08:00
weight = 23
type = "docs"
description = "01-解答 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/types-and-values/solution.html](https://google.github.io/comprehensive-rust/types-and-values/solution.html)

# 3.6.1 解答

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn fib(n: u32) -> u32 {
    if n < 2 {
        return n;
    } else {
        return fib(n - 1) + fib(n - 2);
    }
}

fn main() {
    let n = 20;
    println!("fib({n}) = {}", fib(n));
}
```

这里我们用 `return` 语法从函数返回值。课程稍后会看到：代码块中最后一个表达式会自动作为返回值，
从而可以省略 `return` 关键字，写出更简洁的风格。

`if` 条件 `n < 2` 不需要括号，这是标准的 Rust 风格。

## Panic

练习问这个函数何时会 panic。斐波那契数列增长非常快。使用 `u32` 时，当 `n` 达到 48，
计算结果会溢出 32 位整数上限（4,294,967,295）。

在 Rust 中，整数运算在 _debug 模式_（使用 `cargo run` 时的默认模式）下会检查溢出。
若发生溢出，程序会 panic（带错误信息崩溃）。在 _release 模式_（`cargo run --release`）下，
溢出检查默认关闭，数值会环绕（模运算），产生错误结果。

> - 逐步讲解解答。
> - 解释递归调用如何得到最终结果。
> - 讨论整数溢出问题。使用 `u32` 时，大约在 `n` 为 47 附近函数会 panic。可以把 `main` 的输入改掉来演示。
> - 展示迭代解法作为替代，并比较其与递归在性能和内存使用上的差异。迭代解法会高效得多。
>
> ## 延伸阅读
>
> 若要更进阶讨论，可以介绍记忆化（memoization）或动态规划来优化递归斐波那契计算，
> 不过这已超出当前主题范围。

