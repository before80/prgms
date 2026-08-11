+++
title = "7.2.9 其他类型"
date = 2026-08-11T11:30:00+08:00
weight = 250
type = "docs"
description = "09-其他类型 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability/cpp/type-mapping.html](https://google.github.io/comprehensive-rust/android/interoperability/cpp/type-mapping.html)

# 7.2.9 其他类型

| Rust 类型         | C++ 类型             |
| ----------------- | -------------------- |
| `String`          | `rust::String`       |
| `&str`            | `rust::Str`          |
| `CxxString`       | `std::string`        |
| `&[T]`/`&mut [T]` | `rust::Slice`        |
| `Box<T>`          | `rust::Box<T>`       |
| `UniquePtr<T>`    | `std::unique_ptr<T>` |
| `Vec<T>`          | `rust::Vec<T>`       |
| `CxxVector<T>`    | `std::vector<T>`     |

> - 这些类型可用于共享结构体的字段，以及 extern 函数的参数与返回值。
> - 注意 Rust 的 `String` 并不直接映射到 `std::string`。原因有几点：
>   - `std::string` 并不维护 `String` 所要求的 UTF-8 不变量。
>   - 两种类型在内存中的布局不同，因此不能在语言之间直接传递。
>   - `std::string` 需要与 Rust 移动语义不匹配的移动构造函数，因此 `std::string` 不能按值传给 Rust。

