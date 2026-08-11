+++
title = "3.5.1 Unsafe Rust 函数"
date = 2026-08-11T11:30:00+08:00
weight = 202
type = "docs"
description = "01-Unsafe Rust 函数 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-rust/unsafe-functions/rust.html](https://google.github.io/comprehensive-rust/unsafe-rust/unsafe-functions/rust.html)

# 3.5.1 Unsafe Rust 函数

若你自己的函数需要特定前置条件才能避免未定义行为，可以将其标记为 `unsafe`。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 交换两个指针所指向的值。
///
/// # Safety
///
/// 指针必须有效、正确对齐，并且在函数调用期间不被以其他方式访问。
unsafe fn swap(a: *mut u8, b: *mut u8) {
    // SAFETY: 调用方承诺指针有效、正确对齐，且无其他访问。
    unsafe {
        let temp = *a;
        *a = *b;
        *b = temp;
    }
}

fn main() {
    let mut a = 42;
    let mut b = 66;

    // SAFETY: 指针来自引用，因此有效、对齐且唯一。
    unsafe {
        swap(&mut a, &mut b);
    }

    println!("a = {}, b = {}", a, b);
}
```

> <summary>讲师备注</summary>
>
> 实际中我们不会用指针写 `swap` 函数——用引用就能安全完成。
>
> 注意：Rust 2021 及更早版本允许在 unsafe 函数内部直接写 unsafe 代码而无需 `unsafe` 块。2024 edition 改变了这一点。在较旧的 edition 中可用 `#[deny(unsafe_op_in_unsafe_fn)]` 禁止这种写法。试着加上它，看看会发生什么。

