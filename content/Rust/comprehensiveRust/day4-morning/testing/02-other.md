+++
title = "4.2 其他类型的测试"
date = 2026-08-11T11:30:00+08:00
weight = 180
type = "docs"
description = "02-其他类型的测试 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/testing/other.html](https://google.github.io/comprehensive-rust/testing/other.html)

# 4.2 其他类型的测试

## 集成测试

若要以客户端身份测试你的库，请使用集成测试。

在 `tests/` 下创建 `.rs` 文件：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
// tests/my_library.rs
use my_library::init;

#[test]
fn test_init() {
    assert!(init().is_ok());
}
```

这些测试只能访问你的 crate 的公共 API。

## 文档测试

Rust 内置支持文档测试：

````rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 将字符串缩短到给定长度。
///
/// ```
/// # use playground::shorten_string;
/// assert_eq!(shorten_string("Hello World", 5), "Hello");
/// assert_eq!(shorten_string("Hello World", 20), "Hello World");
/// ```
pub fn shorten_string(s: &str, length: usize) -> &str {
    &s[..std::cmp::min(length, s.len())]
}
````

- `///` 注释中的代码块会自动被视为 Rust 代码。
- 这些代码会在 `cargo test` 时被编译并执行。
- 在代码前加 `#` 会在文档中隐藏该行，但仍会编译/运行。
- 可在
  [Rust Playground](https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=3ce2ad13ea1302f6572cb15cd96becf0)
  上测试上面的代码。
