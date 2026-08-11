+++
title = "4.1 单元测试"
date = 2026-08-11T11:30:00+08:00
weight = 179
type = "docs"
description = "01-单元测试 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/testing/unit-tests.html](https://google.github.io/comprehensive-rust/testing/unit-tests.html)

# 4.1 单元测试

Rust 与 Cargo 自带简单的单元测试框架。测试用 `#[test]` 标记。单元测试常放在嵌套的 `tests` 模块中，并用 `#[cfg(test)]` 仅在构建测试时条件编译。

```rust
// Copyright 2022 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn first_word(text: &str) -> &str {
    match text.find(' ') {
        Some(idx) => &text[..idx],
        None => &text,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_empty() {
        assert_eq!(first_word(""), "");
    }

    #[test]
    fn test_single_word() {
        assert_eq!(first_word("Hello"), "Hello");
    }

    #[test]
    fn test_multiple_words() {
        assert_eq!(first_word("Hello World"), "Hello");
    }
}
```

- 这样可以对私有辅助函数做单元测试。
- `#[cfg(test)]` 属性仅在运行 `cargo test` 时生效。
