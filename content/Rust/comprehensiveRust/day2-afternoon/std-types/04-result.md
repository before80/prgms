+++
title = "3.4 `Result`"
date = 2026-08-11T11:30:00+08:00
weight = 106
type = "docs"
description = "04-`Result` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/std-types/result.html](https://google.github.io/comprehensive-rust/std-types/result.html)

# 3.4 `Result`

`Result` 与 `Option` 类似，但表示操作的成功或失败，各对应一个不同的枚举变体。它是泛型的：`Result<T, E>`，其中 `T` 用于 `Ok` 变体，`E` 出现在 `Err` 变体中。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::fs::File;
use std::io::Read;

fn main() {
    let file: Result<File, std::io::Error> = File::open("diary.txt");
    match file {
        Ok(mut file) => {
            let mut contents = String::new();
            if let Ok(bytes) = file.read_to_string(&mut contents) {
                println!("Dear diary: {contents} ({bytes} bytes)");
            } else {
                println!("Could not read file content");
            }
        }
        Err(err) => {
            println!("The diary could not be opened: {err}");
        }
    }
}
```

> - 与 `Option` 一样，成功值位于 `Result` 内部，迫使开发者显式取出。这鼓励做错误检查。在错误本不该发生的情况下，可以调用 `unwrap()` 或 `expect()`，这也表达了开发者意图。
> - 建议阅读 `Result` 文档——不必在课上读，但值得一提。它包含许多方便方法和函数，有助于函数式风格编程。
> - `Result` 是实现错误处理的标准类型，我们会在第 4 天看到。

