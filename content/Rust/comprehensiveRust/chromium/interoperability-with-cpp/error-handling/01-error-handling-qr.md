+++
title = "7.3.1 错误处理：QR 示例"
date = 2026-08-11T11:30:00+08:00
weight = 274
type = "docs"
description = "01-错误处理：QR 示例 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/interoperability-with-cpp/error-handling-qr.html](https://google.github.io/comprehensive-rust/chromium/interoperability-with-cpp/error-handling-qr.html)

# 7.3.1 错误处理：QR 示例

QR 码生成器是[一个示例][0]：用布尔值传达成功与失败，且成功结果可以跨 FFI 边界传递：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[cxx::bridge(namespace = "qr_code_generator")]
mod ffi {
    extern "Rust" {
        fn generate_qr_code_using_rust(
            data: &[u8],
            min_version: i16,
            out_pixels: Pin<&mut CxxVector<u8>>,
            out_qr_size: &mut usize,
        ) -> bool;
    }
}
```

> 学员可能对 `out_qr_size` 输出的语义感到好奇。这不是向量的大小，而是 QR 码的大小（而且老实说有点多余——它是向量大小的平方根）。
>
> 值得指出在调用 Rust 函数之前初始化 `out_qr_size` 的重要性。创建指向未初始化内存的 Rust 引用会导致未定义行为（与 C++ 不同，在 C++ 中只有解引用此类内存的行为才导致 UB）。
>
> 若学员问到 `Pin`，则解释为何 CXX 对指向 C++ 数据的可变引用需要它：答案是 C++ 数据不能像 Rust 数据那样移动，因为它可能包含自引用指针。


[0]: https://source.chromium.org/chromium/chromium/src/+/main:components/qr_code_generator/qr_code_generator_ffi_glue.rs;l=13-18;drc=7bf1b75b910ca430501b9c6a74c1d18a0223ecca
