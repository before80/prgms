+++
title = "6.2 Rust 测试的 GN 规则"
date = 2026-08-11T11:30:00+08:00
weight = 267
type = "docs"
description = "02-Rust 测试的 GN 规则 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/testing/build-gn.html](https://google.github.io/comprehensive-rust/chromium/testing/build-gn.html)

# 6.2 Rust 测试的 GN 规则

构建 Rust `gtest` 测试最简单的方式，是把它们加到已包含用 C++ 编写的测试的现有测试二进制中。例如：

```gn
test("ui_base_unittests") {
  ...
  sources += [ "my_rust_lib_unittest.rs" ]
  deps += [ ":my_rust_lib" ]
}
```

把 Rust 测试写在单独的 `static_library` 中也可以，但需要手动声明对支持库的依赖：

```gn
rust_static_library("my_rust_lib_unittests") {
  testonly = true
  is_gtest_unittests = true
  crate_root = "my_rust_lib_unittest.rs"
  sources = [ "my_rust_lib_unittest.rs" ]
  deps = [
    ":my_rust_lib",
    "//testing/rust_gtest_interop",
  ]
}

test("ui_base_unittests") {
  ...
  deps += [ ":my_rust_lib_unittests" ]
}
```
