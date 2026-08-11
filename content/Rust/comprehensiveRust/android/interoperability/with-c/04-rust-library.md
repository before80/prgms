+++
title = "7.1.4 简单的 Rust 库"
date = 2026-08-11T11:30:00+08:00
weight = 239
type = "docs"
description = "04-简单的 Rust 库 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability/with-c/rust-library.html](https://google.github.io/comprehensive-rust/android/interoperability/with-c/rust-library.html)

# 7.1.4 简单的 Rust 库

把 Rust 函数与类型导出到 C 很容易。下面是一个简单的 Rust 库：

_interoperability/rust/libanalyze/analyze.rs_

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
//! Rust FFI 演示。
#![deny(improper_ctypes_definitions)]

use std::os::raw::c_int;

/// 分析这些数字。
// SAFETY: 不存在其他同名的全局函数。
#[unsafe(no_mangle)]
pub extern "C" fn analyze_numbers(x: c_int, y: c_int) {
    if x < y {
        println!("x ({x}) is smallest!");
    } else {
        println!("y ({y}) is probably larger than x ({x})");
    }
}
```

_interoperability/rust/libanalyze/Android.bp_

```javascript
rust_ffi {
    name: "libanalyze_ffi",
    crate_name: "analyze_ffi",
    srcs: ["analyze.rs"],
    include_dirs: ["."],
}
```

> `#[unsafe(no_mangle)]` 会禁用 Rust 通常的名字 mangling，因此导出的符号就是函数名本身。你也可以用 `#[unsafe(export_name = "some_name")]` 指定任意名字。

