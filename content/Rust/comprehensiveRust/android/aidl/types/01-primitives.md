+++
title = "4.2.1 原始类型"
date = 2026-08-11T11:30:00+08:00
weight = 225
type = "docs"
description = "01-原始类型 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/aidl/types/primitives.html](https://google.github.io/comprehensive-rust/android/aidl/types/primitives.html)

# 4.2.1 原始类型

原始类型（大多）按习惯方式映射：

| AIDL 类型 | Rust 类型 | 说明                              |
| --------- | --------- | --------------------------------- |
| `boolean` | `bool`    |                                   |
| `byte`    | `i8`      | 注意 byte 是有符号的。            |
| `char`    | `u16`     | 注意使用的是 `u16`，不是 `u32`。  |
| `int`     | `i32`     |                                   |
| `long`    | `i64`     |                                   |
| `float`   | `f32`     |                                   |
| `double`  | `f64`     |                                   |
| `String`  | `String`  |                                   |
