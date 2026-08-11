+++
title = "4 AIDL"
date = 2026-08-11T11:30:00+08:00
weight = 214
type = "docs"
description = "AIDL — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/aidl.html](https://google.github.io/comprehensive-rust/android/aidl.html)

# 4 AIDL

Rust 支持
[Android Interface Definition Language (AIDL)](https://developer.android.com/guide/components/aidl)：

- Rust 代码可以调用现有的 AIDL 服务端。
- 你可以用 Rust 创建新的 AIDL 服务端。

> - AIDL 使 Android 应用能够彼此交互。
>
> - 由于 Rust 在该生态中是一等公民，设备上的其他进程可以调用 Rust 服务。

