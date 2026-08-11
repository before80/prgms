+++
title = "4.5 `Read` 与 `Write`"
date = 2026-08-11T11:30:00+08:00
weight = 117
type = "docs"
description = "05-`Read` 与 `Write` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/std-traits/read-and-write.html](https://google.github.io/comprehensive-rust/std-traits/read-and-write.html)

# 4.5 `Read` 与 `Write`

使用 [`Read`][1] 与 [`BufRead`][2]，可以对 `u8` 源做抽象：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::io::{BufRead, BufReader, Read, Result};

fn count_lines<R: Read>(reader: R) -> usize {
    let buf_reader = BufReader::new(reader);
    buf_reader.lines().count()
}

fn main() -> Result<()> {
    let slice: &[u8] = b"foo\nbar\nbaz\n";
    println!("lines in slice: {}", count_lines(slice));

    let file = std::fs::File::open(std::env::current_exe()?)?;
    println!("lines in file: {}", count_lines(file));
    Ok(())
}
```

类似地，[`Write`][3] 让你对 `u8` 汇点做抽象：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::io::{Result, Write};

fn log<W: Write>(writer: &mut W, msg: &str) -> Result<()> {
    writer.write_all(msg.as_bytes())?;
    writer.write_all("\n".as_bytes())
}

fn main() -> Result<()> {
    let mut buffer = Vec::new();
    log(&mut buffer, "Hello")?;
    log(&mut buffer, "World")?;
    println!("Logged: {buffer:?}");
    Ok(())
}
```

[1]: https://doc.rust-lang.org/std/io/trait.Read.html
[2]: https://doc.rust-lang.org/std/io/trait.BufRead.html
[3]: https://doc.rust-lang.org/std/io/trait.Write.html
