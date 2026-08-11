+++
title = "7.4 在 Chromium 中使用 CXX"
date = 2026-08-11T11:30:00+08:00
weight = 276
type = "docs"
description = "03-在 Chromium 中使用 CXX — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/interoperability-with-cpp/using-cxx-in-chromium.html](https://google.github.io/comprehensive-rust/chromium/interoperability-with-cpp/using-cxx-in-chromium.html)

# 7.4 在 Chromium 中使用 CXX

## 在 Chromium 中使用 cxx

在 Chromium 中，我们为每个想使用 Rust 的叶节点定义一个独立的 `#[cxx::bridge] mod`。通常每个 `rust_static_library` 会有一个。只需在现有的 `rust_static_library` 目标中，与 `crate_root` 和 `sources` 一起加入：

```gn
cxx_bindings = [ "my_rust_file.rs" ]
   # 包含 #[cxx::bridge] 的文件列表，不是全部源文件
allow_unsafe = true
```

C++ 头文件会生成在合理位置，因此你可以：

```cpp
#include "ui/base/my_rust_file.rs.h"
```

你会在 `//base` 中找到一些工具函数，用于在 Chromium C++ 类型与 CXX Rust 类型之间转换——例如 [`SpanToRustSlice`][0]。

> 学员可能会问——为什么我们仍然需要 `allow_unsafe = true`？
>
> 宽泛的答案是：按通常的 Rust 标准，没有任何 C/C++ 代码是“安全的”。从 Rust 来回调用 C/C++ 可能对内存做任意事情，并损害 Rust 自身数据布局的安全性。在 C/C++ 互操作中出现_太多_ `unsafe` 关键字会损害该关键字的信噪比，而且有[争议][1]，但严格来说，把任何外部代码带入 Rust 二进制，从 Rust 的视角都可能造成意外行为。
>
> 狭义的答案在[本页][2]顶部的图中——在幕后，CXX 会像我们在上一节手工做的那样生成 Rust `unsafe` 与 `extern "C"` 函数。


[0]: https://source.chromium.org/chromium/chromium/src/+/main:base/containers/span_rust.h;l=21
[1]: https://steveklabnik.com/writing/the-cxx-debate
[2]: ../
