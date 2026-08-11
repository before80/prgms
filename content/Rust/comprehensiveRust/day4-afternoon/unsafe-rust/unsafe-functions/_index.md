+++
title = "3.5 Unsafe 函数"
date = 2026-08-11T11:30:00+08:00
weight = 201
type = "docs"
description = "Unsafe 函数 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-rust/unsafe-functions.html](https://google.github.io/comprehensive-rust/unsafe-rust/unsafe-functions.html)

# 3.5 Unsafe 函数

若函数或方法有额外前置条件，必须由调用方满足才能避免未定义行为，则可将其标记为 `unsafe`。

Unsafe 函数可能来自两处：

- 声明为 unsafe 的 Rust 函数。
- `extern "C"` 块中的 unsafe 外部函数。

> <summary>讲师备注</summary>
>
> 接下来我们分别看这两种 unsafe 函数。

