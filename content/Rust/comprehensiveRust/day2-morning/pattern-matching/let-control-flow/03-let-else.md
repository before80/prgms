+++
title = "2.5.3 `let else`"
date = 2026-08-11T11:30:00+08:00
weight = 73
type = "docs"
description = "03-`let else` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/pattern-matching/let-control-flow/let-else.html](https://google.github.io/comprehensive-rust/pattern-matching/let-control-flow/let-else.html)

# 2.5.3 `let else`

对于「匹配某个模式，否则从函数返回」这种常见情况，使用
[`let else`](https://doc.rust-lang.org/rust-by-example/flow_control/let_else.html)。
「else」分支必须发散（`return`、`break` 或 panic——除了落到块末尾之外的任何做法）。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn hex_or_die_trying(maybe_string: Option<String>) -> Result<u32, String> {
    let s = if let Some(s) = maybe_string {
        s
    } else {
        return Err(String::from("got None"));
    };

    let first_byte_char = if let Some(first) = s.chars().next() {
        first
    } else {
        return Err(String::from("got empty string"));
    };

    let digit = if let Some(digit) = first_byte_char.to_digit(16) {
        digit
    } else {
        return Err(String::from("not a hex digit"));
    };

    Ok(digit)
}

fn main() {
    println!("result: {:?}", hex_or_die_trying(Some(String::from("foo"))));
}
```

> 改写后的版本是：
>
> ```rust
> // Copyright 2025 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> fn hex_or_die_trying(maybe_string: Option<String>) -> Result<u32, String> {
>     let Some(s) = maybe_string else {
>         return Err(String::from("got None"));
>     };
>
>     let Some(first_byte_char) = s.chars().next() else {
>         return Err(String::from("got empty string"));
>     };
>
>     let Some(digit) = first_byte_char.to_digit(16) else {
>         return Err(String::from("not a hex digit"));
>     };
>
>     Ok(digit)
> }
> ```
>
> ## 深入探索
>
> - 这种基于提前返回的控制流在 Rust 错误处理中很常见：尝试从 `Result` 取出值，若为 `Err` 则返回错误。
> - 若学员问起，也可以演示真实错误处理代码如何用 `?` 来写。

