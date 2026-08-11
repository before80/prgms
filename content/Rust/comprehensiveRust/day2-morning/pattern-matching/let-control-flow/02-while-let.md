+++
title = "2.5.2 `while let` 语句"
date = 2026-08-11T11:30:00+08:00
weight = 72
type = "docs"
description = "02-`while let` 语句 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/pattern-matching/let-control-flow/while-let.html](https://google.github.io/comprehensive-rust/pattern-matching/let-control-flow/while-let.html)

# 2.5.2 `while let` 语句

与 `if let` 类似，还有
[`while let`](https://doc.rust-lang.org/reference/expressions/loop-expr.html#predicate-pattern-loops)
变体，会反复把值与模式进行测试：

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let mut name = String::from("Comprehensive Rust 🦀");
    while let Some(c) = name.pop() {
        dbg!(c);
    }
    // （反转字符串还有更高效的方式！）
}
```

这里
[`String::pop`](https://doc.rust-lang.org/stable/std/string/struct.String.html#method.pop)
在字符串非空时返回 `Some(c)`，为空后返回 `None`。`while let` 让我们持续迭代所有项。

> - 指出：只要值匹配模式，`while let` 循环就会继续。
> - 可以把 `while let` 循环改写成无限循环，再用 `if` 在 `name.pop()` 没有可解包的值时 `break`。`while let` 是上述场景的语法糖。
> - 这种形式不能作为表达式使用，因为条件为假时可能没有值。

