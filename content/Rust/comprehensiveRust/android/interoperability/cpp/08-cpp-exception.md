+++
title = "7.2.8 C++ 错误处理"
date = 2026-08-11T11:30:00+08:00
weight = 249
type = "docs"
description = "08-C++ 错误处理 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability/cpp/cpp-exception.html](https://google.github.io/comprehensive-rust/android/interoperability/cpp/cpp-exception.html)

# 7.2.8 C++ 错误处理

```rust,ignore
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[cxx::bridge]
mod ffi {
    unsafe extern "C++" {
        include!("example/include/example.h");
        fn fallible(depth: usize) -> Result<String>;
    }
}

fn main() {
    if let Err(err) = ffi::fallible(99) {
        eprintln!("Error: {}", err);
        process::exit(1);
    }
}
```

> - 声明为返回 `Result` 的 C++ 函数会在 C++ 一侧捕获任何抛出的异常，并将其作为 `Err` 值返回给调用的 Rust 函数。
> - 若异常从 CXX 桥接未声明返回 `Result` 的 extern "C++" 函数抛出，程序会调用 C++ 的 `std::terminate`。行为等价于同一异常穿过一个 `noexcept` C++ 函数。

