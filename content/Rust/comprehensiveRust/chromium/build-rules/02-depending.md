+++
title = "5.2 从 Chromium C++ 依赖 Rust 代码"
date = 2026-08-11T11:30:00+08:00
weight = 262
type = "docs"
description = "02-从 Chromium C++ 依赖 Rust 代码 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/build-rules/depending.html](https://google.github.io/comprehensive-rust/chromium/build-rules/depending.html)

# 5.2 从 Chromium C++ 依赖 Rust 代码

只需把上述目标加到某个 Chromium C++ 目标的 `deps` 中。

```gn
import("//build/rust/rust_static_library.gni")

rust_static_library("my_rust_lib") {
  crate_root = "lib.rs"
  sources = [ "lib.rs" ]
}

# 也可以是 source_set、static_library 等。
component("preexisting_cpp") {
  deps = [ ":my_rust_lib" ]
}
```

> 我们会看到，只有当 Rust 代码暴露可从 C++ 调用的纯 C API，或我们使用 C++/Rust 互操作工具时，这种关系才有效。

