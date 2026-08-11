+++
title = "4.2.2 数组类型"
date = 2026-08-11T11:30:00+08:00
weight = 226
type = "docs"
description = "02-数组类型 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/aidl/types/arrays.html](https://google.github.io/comprehensive-rust/android/aidl/types/arrays.html)

# 4.2.2 数组类型

数组类型（`T[]`、`byte[]` 与 `List<T>`）会根据它们在函数签名中的用法，翻译成合适的 Rust 数组类型：

| 位置                   | Rust 类型     |
| ---------------------- | ------------- |
| `in` 参数              | `&[T]`        |
| `out`/`inout` 参数     | `&mut Vec<T>` |
| 返回值                 | `Vec<T>`      |

> - 在 Android 13 或更高版本中，支持固定大小数组，即 `T[N]` 变为 `[T; N]`。固定大小数组可以有多个维度（例如 `int[3][4]`）。在 Java 后端，固定大小数组表示为数组类型。
> - parcelable 字段中的数组总是翻译为 `Vec<T>`。

