+++
title = "第3章 自定义类型"
date = 2026-08-20T21:20:00+08:00
weight = 14
type = "docs"
description = "自定义类型 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/custom_types.html](https://doc.rust-lang.org/stable/rust-by-example/custom_types.html)

# 自定义类型

Rust 自定义数据类型主要是通过下面这两个关键字来创建：

* `struct`： 定义一个结构体（structure）
* `enum`： 定义一个枚举类型（enumeration）

而常量（constant）可以通过 `const` 和 `static` 关键字来创建。
