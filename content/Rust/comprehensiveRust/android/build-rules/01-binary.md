+++
title = "3.1 二进制"
date = 2026-08-11T11:30:00+08:00
weight = 212
type = "docs"
description = "01-二进制 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/build-rules/binary.html](https://google.github.io/comprehensive-rust/android/build-rules/binary.html)

# 3.1 二进制

先从一个简单应用开始。在 AOSP 检出根目录创建以下文件：

_hello_rust/Android.bp_：

```javascript
rust_binary {
    name: "hello_rust",
    crate_name: "hello_rust",
    srcs: ["src/main.rs"],
}
```

_hello_rust/src/main.rs_：

```rust
// Copyright 2022 Google LLC
// SPDX-License-Identifier: Apache-2.0
//! Rust demo.

/// Prints a greeting to standard output.
fn main() {
    println!("Hello from Rust!");
}
```

现在可以构建、推送并运行该二进制：

```shell
m hello_rust
adb push "$ANDROID_PRODUCT_OUT/system/bin/hello_rust" /data/local/tmp
adb shell /data/local/tmp/hello_rust
```

```text
Hello from Rust!
```

> - 走一遍构建步骤，并在模拟器中演示运行。
>
> - 注意到大量文档注释了吗？Android 构建规则要求所有模块都有文档。试试删掉它，看看会得到什么错误。
>
> - 强调 Rust 构建规则与其他 Soong 规则外观一致。这是刻意设计，让使用 Rust 与使用 C++ 或 Java 一样容易。

