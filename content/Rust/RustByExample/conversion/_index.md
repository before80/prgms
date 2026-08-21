+++
title = "第6章 类型转换"
date = 2026-08-20T21:20:00+08:00
weight = 31
type = "docs"
description = "类型转换 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/conversion.html](https://doc.rust-lang.org/stable/rust-by-example/conversion.html)

# 类型转换

Rust 使用 [trait][traits] 解决类型之间的转换问题。最一般的转换会用到 [`From`] 和 [`Into`] 两个 trait。不过，即便常见的情况也可能会用到特别的 trait，尤其是从 `String` 转换到别的类型，以及把别的类型转换到 `String` 时。

[traits]: ../trait/
[`From`]: https://rustwiki.org/zh-CN/std/convert/trait.From.html
[`Into`]: https://rustwiki.org/zh-CN/std/convert/trait.Into.html
