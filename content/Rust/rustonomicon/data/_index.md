+++
title = "第2章 数据布局"
date = 2026-08-06T17:08:00+08:00
weight = 6
type = "docs"
description = "Rust 中数据的内存表示与布局"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 数据布局


> 原文链接: [https://doc.rust-lang.org/nomicon/data.html](https://doc.rust-lang.org/nomicon/data.html)


　　底层编程非常在意数据布局，这是大事，也广泛影响语言其余部分，因此我们从 Rust 中数据如何表示讲起。

　　本章 理想情况下 应与 Reference 的 [Type Layout 一节][ref-type-layout] 一致，并因之显得多余。本书初写时 Reference 完全失修，Rustonomicon 试图部分替代 Reference。情况已非如此，整章 理想情况下 可删除。

　　我们会再保留本章一段时间，但 理想情况下 你应把新事实或改进贡献给 Reference。

[ref-type-layout]: ../reference/type-layout.html
