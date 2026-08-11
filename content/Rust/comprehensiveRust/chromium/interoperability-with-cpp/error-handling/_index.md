+++
title = "7.3 CXX 错误处理"
date = 2026-08-11T11:30:00+08:00
weight = 273
type = "docs"
description = "CXX 错误处理 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/interoperability-with-cpp/error-handling.html](https://google.github.io/comprehensive-rust/chromium/interoperability-with-cpp/error-handling.html)

# 7.3 CXX 错误处理

CXX 对 [`Result<T,E>` 的支持][0]依赖 C++ 异常，因此我们不能在 Chromium 中使用它。替代方案：

- `Result<T, E>` 的 `T` 部分可以：
  - 通过输出参数返回（例如通过 `&mut T`）。这要求 `T` 能跨 FFI 边界传递——例如 `T` 必须是：
    - 原始类型（如 `u32` 或 `usize`）
    - `cxx` 原生支持、且在失败情形有合适默认值的类型（如 `UniquePtr<T>`）（_不像_ `Box<T>`）。
  - 保留在 Rust 一侧，并通过引用暴露。当 `T` 是不能跨 FFI 边界传递、也不能存储在 `UniquePtr<T>` 中的 Rust 类型时，可能需要这样做。

- `Result<T, E>` 的 `E` 部分可以：
  - 作为布尔值返回（例如 `true` 表示成功，`false` 表示失败）
  - 保留错误细节在理论上是可能的，但到目前为止实践中尚未需要。

[0]: https://cxx.rs/binding/result.html
