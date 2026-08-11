+++
title = "3.4 同时借用两者"
date = 2026-08-11T11:30:00+08:00
weight = 154
type = "docs"
description = "04-同时借用两者 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/lifetimes/borrow-both.html](https://google.github.io/comprehensive-rust/lifetimes/borrow-both.html)

# 3.4 同时借用两者

本例中，函数可能返回 `a` 或 `b`。我们用生命周期标注告诉编译器：两个借用都可能流入返回值。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn pick<'a>(c: bool, a: &'a i32, b: &'a i32) -> &'a i32 {
    if c { a } else { b }
}

fn main() {
    let mut a = 5;
    let mut b = 10;

    let r = pick(true, &a, &b);

    // Which one is still borrowed?
    // Should either mutation be allowed?
    // a += 7;
    // b += 7;

    dbg!(r);
}
```

> - `pick` 函数会根据 `c` 的值返回 `a` 或 `b`，这意味着我们在编译期无法知道会返回哪一个。
>
> - 为了向编译器表达这一点，我们为 `a` 与 `b` 以及返回类型使用相同的生命周期。这意味着返回的引用会同时借用 `a` _和_ `b`！
>
> - 取消注释那两行被注释的代码，展示即使运行时只会指向其中一个，`r` 也会同时借用 `a` 与 `b`。
>
> - 更改传给 `pick` 的第一个参数，展示无论返回 `a` 还是 `b`，结果都相同。

