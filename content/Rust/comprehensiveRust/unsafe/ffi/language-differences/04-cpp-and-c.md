+++
title = "9.4.4 C++ 与 C"
date = 2026-08-11T11:30:00+08:00
weight = 569
type = "docs"
description = "04-C++ 与 C — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/language-differences/cpp-and-c.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/language-differences/cpp-and-c.html)

# 9.4.4 C++ 与 C

| 关注点 | C | C++ |
| --- | --- | --- |
| **重载** | 手动/临时方案 | 自动 |
| **异常** | - | 栈展开 |
| **析构函数** | 手动清理 | 通过析构函数自动（RAII） |
| **非 POD 类型** | - | 带构造函数、虚表、虚基类的对象 |
| **模板** | - | 编译期代码生成 |

> C++ 包含许多 C 中不存在的、会影响 FFI 的特性：
>
> 重载：由于名称修饰（name mangling），重载无法表达。
>
> 异常：必须在 FFI 边界捕获异常并转换为错误码，因为在 `extern "C"` 函数中逃逸的异常属于未定义行为。
>
> 析构函数：C 调用方不会运行析构函数；必须暴露显式的 `*_destroy()` 函数。
>
> 非 POD 类型：跨 FFI 边界必须使用不透明指针，按值传递没有意义。
>
> 模板：无法直接暴露；必须显式实例化并包装每个特化。

