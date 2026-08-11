+++
title = "3.3 值"
date = 2026-08-11T11:30:00+08:00
weight = 19
type = "docs"
description = "03-值 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/types-and-values/values.html](https://google.github.io/comprehensive-rust/types-and-values/values.html)

# 3.3 值

以下是一些基本内置类型，以及各类型字面量的语法。

|                        | 类型                                       | 字面量                         |
| ---------------------- | ------------------------------------------ | ------------------------------ |
| 有符号整数             | `i8`, `i16`, `i32`, `i64`, `i128`, `isize` | `-10`, `0`, `1_000`, `123_i64` |
| 无符号整数             | `u8`, `u16`, `u32`, `u64`, `u128`, `usize` | `0`, `123`, `10_u16`           |
| 浮点数                 | `f32`, `f64`                               | `3.14`, `-10.0e20`, `2_f32`    |
| Unicode 标量值         | `char`                                     | `'a'`, `'α'`, `'∞'`            |
| 布尔值                 | `bool`                                     | `true`, `false`                |

各类型宽度如下：

- `iN`、`uN` 与 `fN` 宽度为 _N_ 位，
- `isize` 与 `usize` 为指针宽度，
- `char` 为 32 位，
- `bool` 为 8 位。

> 还有一些上表未展示的语法：
>
> - 数字中的下划线都可以省略，它们仅用于提高可读性。因此
>   `1_000` 可写成 `1000`（或 `10_00`），`123_i64` 可写成
>   `123i64`。

