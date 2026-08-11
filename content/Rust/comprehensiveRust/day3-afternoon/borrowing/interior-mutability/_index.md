+++
title = "2.4 内部可变性"
date = 2026-08-11T11:30:00+08:00
weight = 145
type = "docs"
description = "内部可变性 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/borrowing/interior-mutability.html](https://google.github.io/comprehensive-rust/borrowing/interior-mutability.html)

# 2.4 内部可变性

在某些情况下，需要通过共享（只读）引用修改数据。例如，共享数据结构可能有内部缓存，并希望从只读方法更新该缓存。

「内部可变性」（interior mutability）模式允许在共享引用背后进行独占（可变）访问。标准库提供了若干实现方式，同时仍保证安全，通常通过运行时检查做到。

> 本页要带走的核心信息是：Rust 提供了在共享引用背后修改数据的_安全_方式。保证安全的方式有多种，接下来的子页会介绍其中几种。

