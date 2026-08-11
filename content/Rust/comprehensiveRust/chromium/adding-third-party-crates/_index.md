+++
title = "8 添加第三方 Crate"
date = 2026-08-11T11:30:00+08:00
weight = 278
type = "docs"
description = "添加第三方 Crate — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates.html](https://google.github.io/comprehensive-rust/chromium/adding-third-party-crates.html)

# 8 添加第三方 Crate

Rust 库称为 “crate”，可在 [crates.io][0] 找到。Rust crate 彼此依赖_非常容易_。所以它们确实会依赖！

| 属性                    | C++ 库      | Rust crate               |
| ----------------------- | ----------- | ------------------------ |
| 构建系统                | 多种多样    | 一致：`Cargo.toml`       |
| 典型库大小              | 偏大        | 小                       |
| 传递依赖                | 少          | 多                       |

对 Chromium 工程师来说，这有利有弊：

- 所有 crate 使用共同的构建系统，因此我们可以自动化它们纳入 Chromium……
- ……但是，crate 通常有传递依赖，因此你很可能需要引入多个库。

我们将讨论：

- 如何把 crate 放进 Chromium 源码树
- 如何为其制作 `gn` 构建规则
- 如何审计其源码以确保足够安全。

[0]: https://crates.io

> 本页表格中的所有内容都是概括，也可以找到反例。但总的来说，重要的是让学员理解：大多数 Rust 代码依赖其他 Rust 库，因为这样做很容易，而这既有好处也有代价。

