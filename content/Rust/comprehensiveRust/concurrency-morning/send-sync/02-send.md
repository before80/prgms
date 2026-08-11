+++
title = "4.2 `Send`"
date = 2026-08-11T11:30:00+08:00
weight = 354
type = "docs"
description = "02-`Send` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/concurrency/send-sync/send.html](https://google.github.io/comprehensive-rust/concurrency/send-sync/send.html)

# 4.2 `Send`

> 若把 `T` 值移到另一线程是安全的，则类型 `T` 是 [`Send`][1]。

把所有权移到另一线程的效果是：*析构函数*会在那个线程中运行。因此问题是：何时可以在一个线程中分配值，而在另一个线程中释放它。

[1]: https://doc.rust-lang.org/std/marker/trait.Send.html

> 例如，到 SQLite 库的连接必须只从一个线程访问。

