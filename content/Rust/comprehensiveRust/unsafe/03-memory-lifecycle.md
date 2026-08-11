+++
title = "6 内存生命周期"
date = 2026-08-11T11:30:00+08:00
weight = 538
type = "docs"
description = "03-内存生命周期 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/memory-lifecycle.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/memory-lifecycle.html)

# 6 内存生命周期

随着对象（值）被创建与销毁，内存会经历不同阶段。

| 内存状态 | Safe Rust 可读？ |
| -------- | ---------------- |
| 可用     | 否               |
| 已分配   | 否               |
| 已初始化 | 是               |

> 本节讨论操作系统提供的内存如何成为程序中的有效变量。
>
> 当内存处于可用状态时，操作系统已将其提供给我们的程序。
>
> 当内存被分配时，它就被保留下来，以便写入值。我们称之为未初始化内存。
>
> 当内存被初始化后，从中读取是安全的。

