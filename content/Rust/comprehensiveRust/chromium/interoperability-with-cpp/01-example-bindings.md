+++
title = "7.1 绑定示例"
date = 2026-08-11T11:30:00+08:00
weight = 271
type = "docs"
description = "01-绑定示例 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/interoperability-with-cpp/example-bindings.html](https://google.github.io/comprehensive-rust/chromium/interoperability-with-cpp/example-bindings.html)

# 7.1 绑定示例

CXX 要求整个 C++/Rust 边界在 `.rs` 源码内的 `cxx::bridge` 模块中声明。

```rust,ignore
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[cxx::bridge]
mod ffi {
    extern "Rust" {
        type MultiBuf;

        fn next_chunk(buf: &mut MultiBuf) -> &[u8];
    }

    unsafe extern "C++" {
        include!("example/include/blobstore.h");

        type BlobstoreClient;

        fn new_blobstore_client() -> UniquePtr<BlobstoreClient>;
        fn put(self: &BlobstoreClient, buf: &mut MultiBuf) -> Result<u64>;
    }
}

// Definitions of Rust types and functions go here
```

> 指出：
>
> - 虽然这看起来像普通的 Rust `mod`，但 `#[cxx::bridge]` 过程宏会对它做复杂的事。生成的代码要精巧得多——不过这仍然会在你的代码中产生一个名为 `ffi` 的 `mod`。
> - 在 Rust 中原生支持 C++ 的 `std::unique_ptr`
> - 在 C++ 中原生支持 Rust 切片
> - 从 C++ 到 Rust 的调用，以及 Rust 类型（上半部分）
> - 从 Rust 到 C++ 的调用，以及 C++ 类型（下半部分）
>
> **常见误解：** 看起来像 Rust 在解析 C++ 头文件，但这有误导性。该头文件从不被 Rust 解释，只是为了 C++ 编译器的利益而在生成的 C++ 代码中被 `#include`。

