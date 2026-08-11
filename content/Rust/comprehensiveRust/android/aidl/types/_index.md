+++
title = "4.2 AIDL 类型"
date = 2026-08-11T11:30:00+08:00
weight = 224
type = "docs"
description = "AIDL 类型 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/aidl/types.html](https://google.github.io/comprehensive-rust/android/aidl/types.html)

# 4.2 AIDL 类型

AIDL 类型会翻译成合适的、符合习惯的 Rust 类型：

- 原始类型（大多）映射为符合习惯的 Rust 类型。
- 支持切片、`Vec` 与字符串类型等集合类型。
- 对 AIDL 对象与文件句柄的引用可以在客户端与服务之间发送。
- 完整支持文件句柄与 parcelable。
