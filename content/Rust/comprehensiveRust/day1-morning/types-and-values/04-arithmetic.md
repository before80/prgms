+++
title = "3.4 算术运算"
date = 2026-08-11T11:30:00+08:00
weight = 20
type = "docs"
description = "04-算术运算 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/types-and-values/arithmetic.html](https://google.github.io/comprehensive-rust/types-and-values/arithmetic.html)

# 3.4 算术运算

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn interproduct(a: i32, b: i32, c: i32) -> i32 {
    return a * b + b * c + c * a;
}

fn main() {
    println!("result: {}", interproduct(120, 100, 248));
}
```

> 这是我们第一次看到除 `main` 以外的函数，但含义应当清楚：它接收三个整数，返回一个整数。
> 函数稍后会更详细讲解。
>
> 算术运算与其他语言非常相似，优先级也相近。
>
> 整数溢出呢？在 C 和 C++ 中，_有符号_整数溢出实际上是未定义行为，运行时可能做出未知事情。
> 在 Rust 中，它是有定义的。
>
> 把 `i32` 改成 `i16` 可以看到整数溢出：在 debug 构建中会 panic（检查），在 release 构建中会环绕。
> 还有其他选项，例如 overflowing、saturating、carrying。通过方法语法访问，例如
> `(a * b).saturating_add(b * c).saturating_add(c * a)`。
>
> 实际上，编译器会检测常量表达式的溢出，因此本例需要使用单独的函数。

