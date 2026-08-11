+++
title = "2.5 `Error` Trait"
date = 2026-08-11T11:30:00+08:00
weight = 191
type = "docs"
description = "05-`Error` Trait — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/error-handling/error.html](https://google.github.io/comprehensive-rust/error-handling/error.html)

# 2.5 `Error` Trait

有时我们希望允许返回任意类型的错误，而不自己写一个枚举去覆盖所有可能。`std::error::Error` trait 让你可以轻松创建能容纳任意错误的 trait 对象。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::error::Error;
use std::fs;
use std::io::Read;

fn read_count(path: &str) -> Result<i32, Box<dyn Error>> {
    let mut count_str = String::new();
    fs::File::open(path)?.read_to_string(&mut count_str)?;
    let count: i32 = count_str.parse()?;
    Ok(count)
}

fn main() {
    fs::write("count.dat", "1i3").unwrap();
    match read_count("count.dat") {
        Ok(count) => println!("Count: {count}"),
        Err(err) => println!("Error: {err}"),
    }
}
```

> <summary>讲师备注</summary>
>
> `read_count` 可能返回 `std::io::Error`（来自文件操作）或 `std::num::ParseIntError`（来自 `String::parse`）。
>
> 把错误装箱（boxing）可以少写代码，但会失去在程序里干净地区分不同错误情形的能力。因此，在库的公共 API 中一般不宜使用 `Box<dyn Error>`；但在只想把错误信息显示出来的应用程序中，它可能是不错的选择。
>
> 定义自定义错误类型时，务必实现 `std::error::Error` trait，以便它能被装箱。

