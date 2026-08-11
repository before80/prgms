+++
title = "7.2.1 桥接模块"
date = 2026-08-11T11:30:00+08:00
weight = 242
type = "docs"
description = "01-桥接模块 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability/cpp/bridge.html](https://google.github.io/comprehensive-rust/android/interoperability/cpp/bridge.html)

# 7.2.1 桥接模块

CXX 依赖对将从每种语言向另一种语言暴露的函数签名的描述。你在一个用 `#[cxx::bridge]` 属性宏标注的 Rust 模块中，通过 extern 块提供该描述。

```rust,ignore
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[allow(unsafe_op_in_unsafe_fn)]
#[cxx::bridge(namespace = "org::blobstore")]
mod ffi {
    // Shared structs with fields visible to both languages.
    struct BlobMetadata {
        size: usize,
        tags: Vec<String>,
    }

    // Rust types and signatures exposed to C++.
    extern "Rust" {
        type MultiBuf;

        fn next_chunk(buf: &mut MultiBuf) -> &[u8];
    }

    // C++ types and signatures exposed to Rust.
    unsafe extern "C++" {
        include!("include/blobstore.h");

        type BlobstoreClient;

        fn new_blobstore_client() -> UniquePtr<BlobstoreClient>;
        fn put(self: Pin<&mut BlobstoreClient>, parts: &mut MultiBuf) -> u64;
        fn tag(self: Pin<&mut BlobstoreClient>, blobid: u64, tag: &str);
        fn metadata(&self, blobid: u64) -> BlobMetadata;
    }
}
```

> - 桥接一般声明在 crate 内的 `ffi` 模块中。
> - 根据桥接模块中的声明，CXX 会生成匹配的 Rust 与 C++ 类型/函数定义，以便将这些项暴露给两种语言。
> - 要查看生成的 Rust 代码，使用 [cargo-expand] 查看展开后的 proc macro。对大多数示例你会用 `cargo expand ::ffi` 只展开 `ffi` 模块（不过这不适用于 Android 项目）。
> - 要查看生成的 C++ 代码，请查看 `target/cxxbridge`。
>
> [cargo-expand]: https://github.com/dtolnay/cargo-expand

