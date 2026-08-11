+++
title = "7.2.12 为 Android 构建：Rust"
date = 2026-08-11T11:30:00+08:00
weight = 253
type = "docs"
description = "12-为 Android 构建：Rust — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability/cpp/android-build-rust.html](https://google.github.io/comprehensive-rust/android/interoperability/cpp/android-build-rust.html)

# 7.2.12 为 Android 构建：Rust

创建一个依赖 `libcxx` 与你的 `cc_library_static` 的 `rust_binary`。

```javascript
rust_binary {
    name: "cxx_test",
    srcs: ["lib.rs"],
    rustlibs: ["libcxx"],
    static_libs: ["libcxx_test_cpp"],
}
```
