+++
title = "2.6 `thiserror`"
date = 2026-08-11T11:30:00+08:00
weight = 192
type = "docs"
description = "06-`thiserror` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/error-handling/thiserror.html](https://google.github.io/comprehensive-rust/error-handling/thiserror.html)

# 2.6 `thiserror`

[`thiserror`](https://docs.rs/thiserror/) crate 提供宏，帮助在定义错误类型时减少样板代码。它提供的 derive 宏可协助实现 `From<T>`、`Display` 以及 `Error` trait。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::io::Read;
use std::{fs, io};
use thiserror::Error;

#[derive(Debug, Error)]
enum ReadUsernameError {
    #[error("I/O error: {0}")]
    IoError(#[from] io::Error),
    #[error("Found no username in {0}")]
    EmptyUsername(String),
}

fn read_username(path: &str) -> Result<String, ReadUsernameError> {
    let mut username = String::with_capacity(100);
    fs::File::open(path)?.read_to_string(&mut username)?;
    if username.is_empty() {
        return Err(ReadUsernameError::EmptyUsername(String::from(path)));
    }
    Ok(username)
}

fn main() {
    //fs::write("config.dat", "").unwrap();
    match read_username("config.dat") {
        Ok(username) => println!("Username: {username}"),
        Err(err) => println!("Error: {err}"),
    }
}
```

> <summary>讲师备注</summary>
>
> - `Error` derive 宏由 `thiserror` 提供，带有大量实用属性，便于紧凑地定义错误类型。
> - `#[error]` 中的消息用于派生 `Display` trait。
> - 注意：(`thiserror::`)`Error` derive 宏虽然会实现 (`std::error::`)`Error` trait，但二者并非同一事物；trait 与宏不共享命名空间。

