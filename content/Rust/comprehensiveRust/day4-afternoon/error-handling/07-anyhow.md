+++
title = "2.7 `anyhow`"
date = 2026-08-11T11:30:00+08:00
weight = 193
type = "docs"
description = "07-`anyhow` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/error-handling/anyhow.html](https://google.github.io/comprehensive-rust/error-handling/anyhow.html)

# 2.7 `anyhow`

[`anyhow`] crate 提供功能丰富的错误类型，支持附带额外上下文信息，从而可以对程序在出错前正在做什么给出语义化追踪。

它可以与 [`thiserror`] 的便利宏结合使用，避免为自定义错误类型显式写出 trait 实现。

[`anyhow`]: https://docs.rs/anyhow/
[`thiserror`]: https://docs.rs/thiserror/

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use anyhow::{Context, Result, bail};
use std::fs;
use std::io::Read;
use thiserror::Error;

#[derive(Clone, Debug, Eq, Error, PartialEq)]
#[error("Found no username in {0}")]
struct EmptyUsernameError(String);

fn read_username(path: &str) -> Result<String> {
    let mut username = String::with_capacity(100);
    fs::File::open(path)
        .with_context(|| format!("Failed to open {path}"))?
        .read_to_string(&mut username)
        .context("Failed to read")?;
    if username.is_empty() {
        bail!(EmptyUsernameError(path.to_string()));
    }
    Ok(username)
}

fn main() {
    //fs::write("config.dat", "").unwrap();
    match read_username("config.dat") {
        Ok(username) => println!("Username: {username}"),
        Err(err) => println!("Error: {err:?}"),
    }
}
```

> <summary>讲师备注</summary>
>
> - `anyhow::Error` 本质上是对 `Box<dyn Error>` 的包装。因此它通常也不适合作为库的公共 API，但在应用程序中被广泛使用。
> - `anyhow::Result<V>` 是 `Result<V, anyhow::Error>` 的类型别名。
> - `anyhow::Error` 提供的功能对 Go 开发者可能很熟悉：行为类似 Go 的 `error` 类型，而 `Result<T, anyhow::Error>` 很像 Go 的 `(T, error)`（约定上这对值中只有一个元素有意义）。
> - `anyhow::Context` 是为标准库的 `Result` 和 `Option` 实现的 trait。需要 `use anyhow::Context`，才能在这些类型上启用 `.context()` 和 `.with_context()`。
>
> # 延伸阅读
>
> - `anyhow::Error` 支持向下转换（downcast），类似 `std::any::Any`；若需要，可用 [`Error::downcast`](https://docs.rs/anyhow/latest/anyhow/struct.Error.html#method.downcast) 取出内部具体的错误类型加以检查。

