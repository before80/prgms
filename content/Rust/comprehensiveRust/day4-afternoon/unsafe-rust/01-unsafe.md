+++
title = "3.1 Unsafe"
date = 2026-08-11T11:30:00+08:00
weight = 197
type = "docs"
description = "01-Unsafe — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-rust/unsafe.html](https://google.github.io/comprehensive-rust/unsafe-rust/unsafe.html)

# 3.1 Unsafe

Rust 语言分为两部分：

- **Safe Rust（安全 Rust）：** 内存安全，不可能出现未定义行为（undefined behavior）。
- **Unsafe Rust（不安全 Rust）：** 若违反前置条件，可能触发未定义行为。

本课程绝大部分内容是 Safe Rust，但了解 Unsafe Rust 同样重要。

Unsafe 代码应当小而隔离，并仔细文档化其正确性。它应被封装在一层安全的抽象之下。

Unsafe Rust 额外提供五类能力：

- 解引用裸指针（raw pointers）。
- 访问或修改可变静态变量（mutable static）。
- 访问 `union` 字段。
- 调用 `unsafe` 函数，包括 `extern` 函数。
- 实现 `unsafe` trait。

接下来我们会简要介绍这些 unsafe 能力。完整细节请参阅
[《The Rust Book》第 19.1 章](https://doc.rust-lang.org/book/ch19-01-unsafe-rust.html)
以及 [Rustonomicon](https://doc.rust-lang.org/nomicon/)。

> <summary>讲师备注</summary>
>
> Unsafe Rust 并不意味着代码一定不正确。它意味着开发者关闭了部分编译器安全特性，必须自行写出正确代码。也就是说，编译器不再强制执行 Rust 的内存安全规则。

