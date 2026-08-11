+++
title = "3.1 模块"
date = 2026-08-11T11:30:00+08:00
weight = 171
type = "docs"
description = "01-模块 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/modules/modules.html](https://google.github.io/comprehensive-rust/modules/modules.html)

# 3.1 模块

我们已经见过 `impl` 块如何把函数归入某个类型的命名空间。

类似地，`mod` 可以把类型和函数放入命名空间：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
mod foo {
    pub fn do_something() {
        println!("In the foo module");
    }
}

mod bar {
    pub fn do_something() {
        println!("In the bar module");
    }
}

fn main() {
    foo::do_something();
    bar::do_something();
}
```

> - 包（package）提供功能，并包含一个描述如何构建一捆（1 个或多个）crate 的 `Cargo.toml` 文件。
> - Crate 是一棵模块树：二进制 crate 生成可执行文件，库 crate 编译为库。
> - 模块（module）定义组织方式与作用域，是本节的重点。

