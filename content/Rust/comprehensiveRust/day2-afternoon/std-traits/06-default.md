+++
title = "4.6 `Default` 与结构体更新语法"
date = 2026-08-11T11:30:00+08:00
weight = 118
type = "docs"
description = "06-`Default` 与结构体更新语法 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/std-traits/default.html](https://google.github.io/comprehensive-rust/std-traits/default.html)

# 4.6 `Default` 与结构体更新语法

[`Default`][1] trait 为类型产生一个默认值。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug, Default)]
struct Derived {
    x: u32,
    y: String,
    z: Implemented,
}

#[derive(Debug)]
struct Implemented(String);

impl Default for Implemented {
    fn default() -> Self {
        Self("John Smith".into())
    }
}

fn main() {
    let default_struct = Derived::default();
    dbg!(default_struct);

    let almost_default_struct =
        Derived { y: "Y is set!".into(), ..Derived::default() };
    dbg!(almost_default_struct);

    let nothing: Option<Derived> = None;
    dbg!(nothing.unwrap_or_default());
}
```

> - 可以直接实现，也可以通过 `#[derive(Default)]` 派生。
> - 派生实现会生成所有字段都设为其默认值的值。
>   - 这意味着结构体中的所有类型也都必须实现 `Default`。
> - 标准 Rust 类型通常以实现合理值（例如 `0`、`""` 等）的方式实现 `Default`。
> - 部分结构体初始化与 default 配合得很好。
> - Rust 标准库知道类型可以实现 `Default`，并提供使用它的便捷方法。
> - `..` 语法称为[结构体更新语法][2]。


[1]: https://doc.rust-lang.org/std/default/trait.Default.html
[2]: https://doc.rust-lang.org/book/ch05-01-defining-structs.html#creating-instances-from-other-instances-with-struct-update-syntax
