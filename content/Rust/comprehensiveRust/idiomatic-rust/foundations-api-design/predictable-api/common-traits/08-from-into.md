+++
title = "2.2.2.8 From 与 Into"
date = 2026-08-11T11:30:00+08:00
weight = 422
type = "docs"
description = "08-From 与 Into — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/from-into.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/from-into.html)

# 2.2.2.8 From 与 Into

从一种类型转换到另一种类型。

可派生：❌，除非使用 `derive_more` 之类 crate。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub struct Wrapper(String);

impl From<&str> for Wrapper {
    fn from(value: &str) -> Self {
        Wrapper(value.to_owned())
    }
}

impl From<i32> for Wrapper {
    fn from(value: i32) -> Self {
        Wrapper(value.to_string())
    }
}

// `Into` 作为 trait bound 用起来更自然。
fn into_string<S: Into<String>>(s: S) {}
fn string_from<T>(t: T) where String: From<T> {}

fn main() {
    // `Wrapper` 可从 `&str` 和 `i32` 构造。
    let a = Wrapper::from("Hello, obvious!");
    let b = Wrapper::from(-123);

    // From 实现隐含 Into 实现。
    let c: Wrapper = "Hello, implementation!".into();
}
```

> - 为类型提供转换功能。
>
> - `From` 提供构造风格函数，而 `Into` 在已有值上提供方法。
>
> - 优先为你撰写的类型写 `From<T>` 实现，而非 `Into<T>`。
>
>   任何实现了 `From` 的类型都会自动实现 `Into`。
>
> - 作为函数参数的 trait bound，更偏好 `Into`，意图更清晰：`T: Into<String>` 比 `String: From<T>` 意图更明确。

