+++
title = "5 构建规则"
date = 2026-08-11T11:30:00+08:00
weight = 260
type = "docs"
description = "构建规则 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/build-rules.html](https://google.github.io/comprehensive-rust/chromium/build-rules.html)

# 5 构建规则

Rust 代码通常用 `cargo` 构建。Chromium 为了效率使用 `gn` 与 `ninja`——其静态规则允许最大并行度。Rust 也不例外。

## 向 Chromium 添加 Rust 代码

在某个现有的 Chromium `BUILD.gn` 文件中，声明一个 `rust_static_library`：

```gn
import("//build/rust/rust_static_library.gni")

rust_static_library("my_rust_lib") {
  crate_root = "lib.rs"
  sources = [ "lib.rs" ]
}
```

你也可以添加对其他 Rust 目标的 `deps`。稍后我们将用它来依赖第三方代码。

> 你必须_同时_指定 crate 根与完整的源文件列表。`crate_root` 是交给 Rust 编译器、表示编译单元根文件的文件——通常是 `lib.rs`。`sources` 是 `ninja` 为确定何时需要重建所需的全部源文件完整列表。
>
> （不存在 Rust `source_set`，因为在 Rust 中，整个 crate 就是一个编译单元。`static_library` 是最小单元。）
>
> 学员可能想知道为何我们需要一个 gn 模板，而不是使用 [gn 对 Rust 静态库的内置支持][0]。答案是该模板提供对 CXX 互操作、Rust features 与单元测试的支持，其中一些我们稍后会用到。


[0]: https://gn.googlesource.com/gn/+/main/docs/reference.md#func_static_library
