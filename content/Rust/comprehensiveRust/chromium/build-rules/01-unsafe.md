+++
title = "5.1 Unsafe 代码"
date = 2026-08-11T11:30:00+08:00
weight = 261
type = "docs"
description = "01-Unsafe 代码 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/build-rules/unsafe.html](https://google.github.io/comprehensive-rust/chromium/build-rules/unsafe.html)

# 5.1 Unsafe 代码

默认情况下，`rust_static_library` 禁止 unsafe Rust 代码——它不会编译。若你需要 unsafe Rust 代码，在 gn 目标中加入 `allow_unsafe = true`。（课程稍后我们会看到必须这样做的情形。）

```gn
import("//build/rust/rust_static_library.gni")

rust_static_library("my_rust_lib") {
  crate_root = "lib.rs"
  sources = [
    "lib.rs",
    "hippopotamus.rs"
  ]
  allow_unsafe = true
}
```
