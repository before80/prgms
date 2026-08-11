+++
title = "第4章 认识所有权"
date = 2026-08-05T08:44:00+08:00
weight = 15
type = "docs"
description = "认识所有权：Rust 如何在没有垃圾回收的前提下保证内存安全"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 认识所有权 {#understanding-ownership}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch04-00-understanding-ownership.html](https://doc.rust-lang.org/stable/book/ch04-00-understanding-ownership.html)


　　所有权（ownership）是 Rust 最独特的特性，并对语言的其余部分有深远影响。正是它让 Rust 能在不依赖垃圾回收器的情况下保证内存安全，因此理解所有权如何工作至关重要。本章会讨论所有权，以及若干相关特性：借用（borrowing）、切片（slice），以及 Rust 如何在内存中排布数据。
