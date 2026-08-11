+++
title = "7 互操作"
date = 2026-08-11T11:30:00+08:00
weight = 234
type = "docs"
description = "互操作 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability.html](https://google.github.io/comprehensive-rust/android/interoperability.html)

# 7 互操作

Rust 对与其他语言的互操作有出色支持。这意味着你可以：

- 从其他语言调用 Rust 函数。
- 从 Rust 调用其他语言编写的函数。

当你调用外部语言中的函数时，你在使用 _foreign function interface_（外部函数接口），也称为 FFI。

> - 这是 Rust 的关键能力：编译后的代码与编译后的 C 或 C++ 代码难以区分。
>
> - 技术上说，Rust 可以编译到与 C 代码相同的 [ABI]（application binary interface，应用程序二进制接口）。


[ABI]: https://en.wikipedia.org/wiki/Application_binary_interface
