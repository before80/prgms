+++
title = "第10章 实现 Arc 与 Mutex"
date = 2026-08-06T17:08:00+08:00
weight = 54
type = "docs"
description = "实现 Arc（与 Mutex 相关讨论）"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 实现 Arc 与 Mutex


> 原文链接: [https://doc.rust-lang.org/nomicon/arc-mutex/arc-and-mutex.html](https://doc.rust-lang.org/nomicon/arc-mutex/arc-and-mutex.html)


　　懂理论固然好，但*最好*的理解方式是亲手实现。为更好理解原子操作与内部可变性（interior mutability），我们将实现标准库 `Arc` 与 `Mutex` 的简化版本。

　　TODO：编写 `Mutex` 章节。
