+++
title = "第13章 内存模型"
date = 2026-08-18T08:45:00+08:00
weight = 102
type = "docs"
description = "内存模型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/memory-model.html](https://doc.rust-lang.org/reference/memory-model.html)

r[memory]
# 内存模型

> **警告**
> Rust 的内存模型尚不完整，也未完全确定。

r[memory.bytes]
## 字节

r[memory.bytes.intro]
Rust 中最基本的内存单位是字节。

> **注意**
> 尽管字节通常会落到硬件字节上，Rust 使用的是一种“抽象”字节概念，可以区分硬件中不存在的差异，例如未初始化，或存储指针的一部分。这些差异可能影响程序是否具有未定义行为，因此它们仍会对已编译的 Rust 程序行为产生切实影响。

r[memory.bytes.contents]
每个字节可以具有下列值之一：

r[memory.bytes.init]
* 一个已初始化字节，包含一个 `u8` 值以及可选的[溯源信息][std::ptr#provenance]，

r[memory.bytes.uninit]
* 一个未初始化字节。

> **注意**
> 上述列表尚不保证是穷尽的。
