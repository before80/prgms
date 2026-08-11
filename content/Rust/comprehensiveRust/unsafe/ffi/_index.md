+++
title = "9 外部函数接口（FFI）"
date = 2026-08-11T11:30:00+08:00
weight = 561
type = "docs"
description = "外部函数接口（FFI） — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi.html)

# 9 外部函数接口（FFI）

本段课程介绍 Rust 的外部函数接口（foreign function interface，FFI）。

大纲：

- 先从包装一个简单的 C 函数开始。
- 再推进到涉及指针与未初始化内存的更复杂情形。
