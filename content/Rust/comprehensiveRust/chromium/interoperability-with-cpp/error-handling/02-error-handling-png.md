+++
title = "7.3.2 错误处理：PNG 示例"
date = 2026-08-11T11:30:00+08:00
weight = 275
type = "docs"
description = "02-错误处理：PNG 示例 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/interoperability-with-cpp/error-handling-png.html](https://google.github.io/comprehensive-rust/chromium/interoperability-with-cpp/error-handling-png.html)

# 7.3.2 错误处理：PNG 示例

PNG 解码器原型说明了当成功结果不能跨 FFI 边界传递时可以怎么做：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[cxx::bridge(namespace = "gfx::rust_bindings")]
mod ffi {
    extern "Rust" {
        /// 这返回 `Result<PngReader<'a>, ()>` 的 FFI 友好等价物。
        fn new_png_reader<'a>(input: &'a [u8]) -> Box<ResultOfPngReader<'a>>;

        /// `crate::png::ResultOfPngReader` 类型的 C++ 绑定。
        type ResultOfPngReader<'a>;
        fn is_err(self: &ResultOfPngReader) -> bool;
        fn unwrap_as_mut<'a, 'b>(
            self: &'b mut ResultOfPngReader<'a>,
        ) -> &'b mut PngReader<'a>;

        /// `crate::png::PngReader` 类型的 C++ 绑定。
        type PngReader<'a>;
        fn height(self: &PngReader) -> u32;
        fn width(self: &PngReader) -> u32;
        fn read_rgba8(self: &mut PngReader, output: &mut [u8]) -> bool;
    }
}
```

> `PngReader` 与 `ResultOfPngReader` 是 Rust 类型——这些类型的对象若不经 `Box<T>` 间接就不能跨 FFI 边界。我们不能有 `out_parameter: &mut PngReader`，因为 CXX 不允许 C++ 按值存储 Rust 对象。
>
> 本例说明：即使 CXX 不支持任意泛型或模板，我们仍可通过手工特化/单态化成非泛型类型，把它们跨 FFI 边界传递。示例中 `ResultOfPngReader` 是一个非泛型类型，它转发到 `Result<T, E>` 的合适方法（例如 `is_err`、`unwrap` 和/或 `as_mut`）。

