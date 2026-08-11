+++
title = "7.2.7 Rust 错误处理"
date = 2026-08-11T11:30:00+08:00
weight = 248
type = "docs"
description = "07-Rust 错误处理 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability/cpp/rust-result.html](https://google.github.io/comprehensive-rust/android/interoperability/cpp/rust-result.html)

# 7.2.7 Rust 错误处理

```rust,ignore
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[cxx::bridge]
mod ffi {
    extern "Rust" {
        fn fallible(depth: usize) -> Result<String>;
    }
}

fn fallible(depth: usize) -> anyhow::Result<String> {
    if depth == 0 {
        return Err(anyhow::Error::msg("fallible1 requires depth > 0"));
    }

    Ok("Success!".into())
}
```

> - 返回 `Result` 的 Rust 函数在 C++ 一侧会翻译成异常。
> - 抛出的异常类型始终是 `rust::Error`，它主要提供获取错误消息字符串的方式。错误消息来自错误类型的 `Display` 实现。
> - 从 Rust 展开到 C++ 的 panic 总会导致进程立即终止。

