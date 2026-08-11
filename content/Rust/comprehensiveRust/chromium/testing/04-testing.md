+++
title = "6.4 练习"
date = 2026-08-11T11:30:00+08:00
weight = 269
type = "docs"
description = "04-练习 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/exercises/chromium/testing.html](https://google.github.io/comprehensive-rust/exercises/chromium/testing.html)

# 6.4 练习

又到练习时间了！

在你的 Chromium 构建中：

- 在 `hello_from_rust` 旁添加一个可测试的函数。一些建议：把作为参数收到的两个整数相加、计算第 n 个斐波那契数、对切片中的整数求和等。
- 添加一个单独的 `..._unittest.rs` 文件，为新函数编写测试。
- 把新测试加到 `BUILD.gn`。
- 构建测试、运行它们，并验证新测试可用。
