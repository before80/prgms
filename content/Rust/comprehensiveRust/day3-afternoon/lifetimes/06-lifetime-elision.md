+++
title = "3.6 生命周期省略"
date = 2026-08-11T11:30:00+08:00
weight = 156
type = "docs"
description = "06-生命周期省略 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/lifetimes/lifetime-elision.html](https://google.github.io/comprehensive-rust/lifetimes/lifetime-elision.html)

# 3.6 生命周期省略

函数参数与返回值的生命周期必须完整指定，但在大多数情况下 Rust 允许按
[几条简单规则](https://doc.rust-lang.org/nomicon/lifetime-elision.html)
省略生命周期。这不是推理（inference）——只是语法简写。

- 每个没有生命周期标注的参数都会获得一个。
- 若只有一个参数生命周期，它会赋给所有未标注的返回值。
- 若有多个参数生命周期，但第一个是 `self`，则该生命周期赋给所有未标注的返回值。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn only_args(a: &i32, b: &i32) {
    todo!();
}

fn identity(a: &i32) -> &i32 {
    a
}

struct Foo(i32);
impl Foo {
    fn get(&self, other: &i32) -> &i32 {
        &self.0
    }
}
```

> - 逐步对每个示例函数应用生命周期省略规则。`only_args` 由第一条规则补全，`identity` 由第二条补全，`Foo::get` 由第三条补全。
>
> - 若应用三条省略规则后仍未填满所有生命周期，你会得到编译错误，要求手动添加标注。

