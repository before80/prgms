+++
title = "6.1 `rust_gtest_interop` 库"
date = 2026-08-11T11:30:00+08:00
weight = 266
type = "docs"
description = "01-`rust_gtest_interop` 库 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/chromium/testing/rust-gtest-interop.html](https://google.github.io/comprehensive-rust/chromium/testing/rust-gtest-interop.html)

# 6.1 `rust_gtest_interop` 库

[`rust_gtest_interop`][0] 库提供了一种方式来：

- 把 Rust 函数用作 `gtest` 测试用例（使用 `#[gtest(...)]` 属性）
- 使用 `expect_eq!` 及类似宏（类似 `assert_eq!`，但不 panic，且断言失败时不终止测试）。

示例：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use rust_gtest_interop::prelude::*;

#[gtest(MyRustTestSuite, MyAdditionTest)]
fn test_addition() {
    expect_eq!(2 + 2, 4);
}
```

[0]: https://chromium.googlesource.com/chromium/src/+/main/testing/rust_gtest_interop/README.md
