+++
title = "3.5.2 Unsafe 外部函数"
date = 2026-08-11T11:30:00+08:00
weight = 203
type = "docs"
description = "02-Unsafe 外部函数 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-rust/unsafe-functions/extern-c.html](https://google.github.io/comprehensive-rust/unsafe-rust/unsafe-functions/extern-c.html)

# 3.5.2 Unsafe 外部函数

可用 `unsafe extern` 声明供 Rust 访问的外部函数。这是 unsafe 的，因为编译器无法推理它们的行为。`extern` 块中声明的函数必须标记为 `safe` 或 `unsafe`，取决于安全使用是否有前置条件：

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::ffi::c_char;

unsafe extern "C" {
    // `abs` 不涉及指针，也没有任何安全要求。
    safe fn abs(input: i32) -> i32;

    /// # Safety
    ///
    /// `s` 必须是指向 NUL 结尾 C 字符串的指针，且在该函数调用期间有效且不被修改。
    unsafe fn strlen(s: *const c_char) -> usize;
}

fn main() {
    println!("Absolute value of -3 according to C: {}", abs(-3));

    unsafe {
        // SAFETY: 我们传入的是 C 字符串字面量的指针，在程序整个生命周期内有效。
        println!("String length: {}", strlen(c"String".as_ptr()));
    }
}
```

> <summary>讲师备注</summary>
>
> - Rust 过去把所有外部函数都视为 unsafe，但自 Rust 1.82 起，随着 `unsafe extern` 块的引入，这一点发生了变化。
> - `abs` 必须显式标记为 `safe`，因为它是外部函数（FFI）。调用外部函数只有在这些函数用指针做可能违反 Rust 内存模型的事情时才成问题；但一般而言，任何 C 函数都可能在任意情况下具有未定义行为。
> - 本例中的 `"C"` 是 ABI；
>   [还有其他可用的 ABI](https://doc.rust-lang.org/reference/items/external-blocks.html)。
> - 注意：Rust 不会验证函数签名是否与实际定义匹配——这取决于你！

