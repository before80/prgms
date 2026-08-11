+++
title = "4.2.8 泛型 vs Trait 对象"
date = 2026-08-11T11:30:00+08:00
weight = 488
type = "docs"
description = "08-泛型 vs Trait 对象 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/dynamic-dispatch/dyn-vs-generics.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/dynamic-dispatch/dyn-vs-generics.html)

# 4.2.8 泛型 vs Trait 对象

我们有两种编写多态函数的方式，它们如何比较？

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn print_display<T: std::fmt::Display>(t: &T) {
    println!("{}", t);
}

fn print_display_dyn(t: &dyn std::fmt::Display) {
    println!("{}", t);
}

fn main() {
    let int = 42i32;
    // 单态化为针对 i32 输入的唯一函数。
    print_display(&int);
    // 每种
    print_display_dyn(&int);
}
```

> - 我们可以用泛型或 trait 对象编写多态函数。
>
> - 编写带泛型参数的函数时，每个替换参数的唯一类型都会生成该函数的一个新版本。
>
>   我们在单态化中讲过：以二进制体积换取更大的优化空间。
>
> - 编写接受 trait 对象的函数时，最终二进制中只会存在该函数的一个版本（不计内联）。
>
> - 泛型参数除二进制体积外是零成本的。类型必须同构（`T` 的所有实例只能是同一类型）。

