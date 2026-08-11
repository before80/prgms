+++
title = "7.2 与 C++ 互操作"
date = 2026-08-11T11:30:00+08:00
weight = 241
type = "docs"
description = "与 C++ 互操作 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability/cpp.html](https://google.github.io/comprehensive-rust/android/interoperability/cpp.html)

# 7.2 与 C++ 互操作

[CXX crate][1] 实现了 Rust 与 C++ 之间的安全互操作。

整体方法如下图：

<img src="img/overview.svg">

[1]: https://cxx.rs/
