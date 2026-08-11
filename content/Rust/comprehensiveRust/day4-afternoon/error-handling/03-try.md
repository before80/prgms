+++
title = "2.3 Try 运算符"
date = 2026-08-11T11:30:00+08:00
weight = 189
type = "docs"
description = "03-Try 运算符 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/error-handling/try.html](https://google.github.io/comprehensive-rust/error-handling/try.html)

# 2.3 Try 运算符

连接被拒绝、文件未找到这类运行时错误用 `Result` 处理，但每次调用都做匹配会很繁琐。Try 运算符 `?` 用于把错误返回给调用方。它能把常见的

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
match some_expression {
    Ok(value) => value,
    Err(err) => return Err(err),
}
```

简化为

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
some_expression?
```

我们可以用它简化错误处理代码：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::io::Read;
use std::{fs, io};

fn read_username(path: &str) -> Result<String, io::Error> {
    let username_file_result = fs::File::open(path);
    let mut username_file = match username_file_result {
        Ok(file) => file,
        Err(err) => return Err(err),
    };

    let mut username = String::new();
    match username_file.read_to_string(&mut username) {
        Ok(_) => Ok(username),
        Err(err) => Err(err),
    }
}

fn main() {
    //fs::write("config.dat", "alice").unwrap();
    let username = read_username("config.dat");
    println!("username or error: {username:?}");
}
```

> <summary>讲师备注</summary>
>
> 请把 `read_username` 改写成使用 `?`。
>
> 要点：
>
> - `username` 变量要么是 `Ok(string)`，要么是 `Err(error)`。
> - 可用 `fs::write` 测试不同场景：无文件、空文件、含用户名的文件。
> - 注意：只要 `E` 实现了 `std::process::Termination`（实践中意味着实现了 `Debug`），`main` 就可以返回 `Result<(), E>`。出错时可执行文件会打印 `Err` 变体并以非零退出码退出。

