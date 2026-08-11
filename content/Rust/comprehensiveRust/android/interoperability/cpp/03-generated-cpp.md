+++
title = "7.2.3 生成的 C++"
date = 2026-08-11T11:30:00+08:00
weight = 244
type = "docs"
description = "03-生成的 C++ — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability/cpp/generated-cpp.html](https://google.github.io/comprehensive-rust/android/interoperability/cpp/generated-cpp.html)

# 7.2.3 生成的 C++

```rust,ignore
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[cxx::bridge]
mod ffi {
    // Rust types and signatures exposed to C++.
    extern "Rust" {
        type MultiBuf;

        fn next_chunk(buf: &mut MultiBuf) -> &[u8];
    }
}
```

大致会得到如下 C++：

```cpp
struct MultiBuf final : public ::rust::Opaque {
  ~MultiBuf() = delete;

private:
  friend ::rust::layout;
  struct layout {
    static ::std::size_t size() noexcept;
    static ::std::size_t align() noexcept;
  };
};

::rust::Slice<::std::uint8_t const> next_chunk(::org::blobstore::MultiBuf &buf) noexcept;
```
