+++
title = "7.2.2 Rust 桥接"
date = 2026-08-11T11:30:00+08:00
weight = 243
type = "docs"
description = "02-Rust 桥接 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability/cpp/rust-bridge.html](https://google.github.io/comprehensive-rust/android/interoperability/cpp/rust-bridge.html)

# 7.2.2 Rust 桥接

```rust,ignore
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[cxx::bridge]
mod ffi {
    extern "Rust" {
        type MyType; // Opaque type
        fn foo(&self); // Method on `MyType`
        fn bar() -> Box<MyType>; // Free function
    }
}

struct MyType(i32);

impl MyType {
    fn foo(&self) {
        println!("{}", self.0);
    }
}

fn bar() -> Box<MyType> {
    Box::new(MyType(123))
}
```

> - `extern "Rust"` 中声明的项引用父模块作用域中的项。
> - CXX 代码生成器使用你的 `extern "Rust"` 区段生成包含对应 C++ 声明的 C++ 头文件。生成的头文件路径与包含桥接的 Rust 源文件相同，只是扩展名为 .rs.h。

