+++
title = "2.4 Try 类型转换"
date = 2026-08-11T11:30:00+08:00
weight = 190
type = "docs"
description = "04-Try 类型转换 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/error-handling/try-conversions.html](https://google.github.io/comprehensive-rust/error-handling/try-conversions.html)

# 2.4 Try 类型转换

`?` 的实际展开比前面说的更复杂一点：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
expression?
```

等价于

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
match expression {
    Ok(value) => value,
    Err(err)  => return Err(From::from(err)),
}
```

这里的 `From::from` 表示尝试把错误类型转换成函数返回类型中的错误类型。这使得把底层错误封装进更高层错误变得很容易。

## 示例

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::error::Error;
use std::io::Read;
use std::{fmt, fs, io};

#[derive(Debug)]
enum ReadUsernameError {
    IoError(io::Error),
    EmptyUsername(String),
}

impl Error for ReadUsernameError {}

impl fmt::Display for ReadUsernameError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Self::IoError(e) => write!(f, "I/O error: {e}"),
            Self::EmptyUsername(path) => write!(f, "Found no username in {path}"),
        }
    }
}

impl From<io::Error> for ReadUsernameError {
    fn from(err: io::Error) -> Self {
        Self::IoError(err)
    }
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
    //std::fs::write("config.dat", "").unwrap();
    let username = read_username("config.dat");
    println!("username or error: {username:?}");
}
```

> <summary>讲师备注</summary>
>
> `?` 运算符必须返回与函数返回类型兼容的值。对 `Result` 而言，意味着错误类型必须兼容：返回 `Result<T, ErrorOuter>` 的函数只能对 `Result<U, ErrorInner>` 使用 `?`，前提是 `ErrorOuter` 与 `ErrorInner` 是同一类型，或 `ErrorOuter` 实现了 `From<ErrorInner>`。
>
> `From` 实现的常见替代方案是 `Result::map_err`，尤其是转换只发生在一处时。
>
> 对 `Option` 没有兼容性要求：返回 `Option<T>` 的函数可以对任意 `T`、`U` 的 `Option<U>` 使用 `?`。
>
> 返回 `Result` 的函数不能对 `Option` 使用 `?`，反之亦然。不过，`Option::ok_or` 可以把 `Option` 转成 `Result`，而 `Result::ok` 可以把 `Result` 转成 `Option`。

