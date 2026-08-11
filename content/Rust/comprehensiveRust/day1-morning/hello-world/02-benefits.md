+++
title = "2.2 Rust 的优势"
date = 2026-08-11T11:30:00+08:00
weight = 14
type = "docs"
description = "02-Rust 的优势 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/hello-world/benefits.html](https://google.github.io/comprehensive-rust/hello-world/benefits.html)

# 2.2 Rust 的优势

Rust 的一些独特卖点：

- _编译期内存安全_ —— 整类内存错误在编译期就被阻止
  - 无未初始化变量。
  - 无双重释放（double-free）。
  - 无释放后使用（use-after-free）。
  - 无 `NULL` 指针。
  - 无忘记解锁的互斥锁。
  - 无线程间数据竞争。
  - 无迭代器失效。

- _无未定义的运行时行为_ —— Rust 语句的行为从不被留作“未指定”
  - 数组访问有边界检查。
  - 整数溢出有明确定义（panic 或环绕）。

- _现代语言特性_ —— 表达力与人体工学媲美更高级语言
  - 枚举与模式匹配（pattern matching）。
  - 泛型（generics）。
  - 零开销 FFI。
  - 零成本抽象。
  - 出色的编译器错误信息。
  - 内置依赖管理器。
  - 内置测试支持。
  - 优秀的 Language Server Protocol 支持。

> 这里不要花太多时间。这些要点后面都会更深入讲解。
>
> 务必询问班级学员有哪些语言经验。根据回答，可以突出 Rust 的不同特性：
>
> - 有 C 或 C++ 经验：Rust 通过借用检查器（borrow checker）消除了整类 _运行时错误_。
>   你能获得与 C/C++ 相当的性能，却没有内存不安全问题。此外，你还能用到模式匹配、
>   内置依赖管理等现代语言构造。
>
> - 有 Java、Go、Python、JavaScript 等经验：你能获得与这些语言同等的内存安全，以及类似的
>   高级语言体验。此外还有像 C/C++ 那样快速且可预测的性能（无垃圾回收），以及在需要时
>   访问底层硬件的能力。

