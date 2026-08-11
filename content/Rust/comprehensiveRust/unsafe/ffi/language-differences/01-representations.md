+++
title = "9.4.1 不同表示"
date = 2026-08-11T11:30:00+08:00
weight = 566
type = "docs"
description = "01-不同表示 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/language-differences/representations.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/language-differences/representations.html)

# 9.4.1 不同表示

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let c_repr = b"Hello, C\0";
    let cc_repr = (b"Hello, C++\0", 10u32);
    let rust_repr = (b"Hello, Rust", 11);
}
```

> 每种语言对实现方式都有自己的主张，可能导致混淆与 bug。考虑三种文本表示方式。
>
> 展示如何将原始表示转换为 Rust 字符串切片：
>
> ```rust
> // Copyright 2026 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> // C 表示转为 Rust
> unsafe {
>     let ptr = c_repr.as_ptr() as *const i8;
>     let c: &str = std::ffi::CStr::from_ptr(ptr).to_str().unwrap();
>     println!("{c}");
> };
>
> // C++ 表示转为 Rust
> unsafe {
>     let ptr = cc_repr.0.as_ptr();
>     let bytes = std::slice::from_raw_parts(ptr, cc_repr.1);
>     let cc: &str = std::str::from_utf8_unchecked(bytes);
>     println!("{cc}");
> };
>
> // Rust 表示（字节）转为字符串切片
> unsafe {
>     let ptr = rust_repr.0.as_ptr();
>     let bytes = std::slice::from_raw_parts(ptr, rust_repr.1);
>     let rust: &str = std::str::from_utf8_unchecked(bytes);
>     println!("{rust}");
> };
> ```
>
> 补充：Rust 有带 `c` 前缀的字符串字面量，会在末尾追加空字节，例如 `c"Rust" == b"Rust\0"`。

