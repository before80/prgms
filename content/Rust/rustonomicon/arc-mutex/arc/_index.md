+++
title = "10.1 Arc"
date = 2026-08-06T17:08:00+08:00
weight = 55
type = "docs"
description = "实现 Arc"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# Arc


> 原文链接: [https://doc.rust-lang.org/nomicon/arc-mutex/arc.html](https://doc.rust-lang.org/nomicon/arc-mutex/arc.html)


　　本节我们将实现 `std::sync::Arc` 的简化版。与[此前实现的 `Vec`](../vec/vec.md)类似，我们不会用到标准库那么多的优化、内建函数或不稳定代码。

　　本实现大致基于标准库实现（技术上取自 1.49 的 `alloc::sync`，因为实际实现在那里），但暂时不支持弱引用（weak reference），因为它们会让实现稍复杂。

　　请注意，本节目前仍在大量编写中。
