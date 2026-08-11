+++
title = "2.2 `Result`"
date = 2026-08-11T11:30:00+08:00
weight = 188
type = "docs"
description = "02-`Result` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/error-handling/result.html](https://google.github.io/comprehensive-rust/error-handling/result.html)

# 2.2 `Result`

Rust 中错误处理的主要机制是 [`Result`] 枚举——我们在讨论标准库类型时已简要见过。

```rust
// Copyright 2022 Google LLC
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

[`Result`]: https://doc.rust-lang.org/stable/std/result/enum.Result.html

> <summary>讲师备注</summary>
>
> - `Result` 有两个变体：`Ok` 承载成功值，`Err` 承载某种错误值。
>
> - 函数是否可能产生错误，通过返回 `Result` 写进类型签名。
>
> - 与 `Option` 类似，你无法“忘记”处理错误：必须先对 `Result` 做模式匹配，确认是哪个变体，才能访问成功值或错误值。`unwrap` 等方法便于写出快速粗糙、不做稳健错误处理的代码，但也意味着源代码里总能看出哪些地方跳过了正确的错误处理。
>
> # 延伸阅读
>
> 把 Rust 的错误处理与学生可能熟悉的其他语言习惯做对比，往往很有帮助。
>
> ## 异常（Exceptions）
>
> - 许多语言使用异常，例如 C++、Java、Python。
>
> - 在多数带异常的语言里，函数是否可能抛异常并不体现在类型签名中。因此调用时通常无法从类型上看出它会不会抛异常。
>
> - 异常一般会展开调用栈，向上传播，直到遇到 `try` 块。深层调用栈中的错误可能影响上层无关的函数。
>
> ## 错误码（Error Numbers）
>
> - 有些语言让函数在成功返回值之外，另行返回错误码（或其他错误值）。例如 C 和 Go。
>
> - 视语言而定，有可能忘记检查错误值，从而访问到未初始化或其他无效的成功值。

