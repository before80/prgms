+++
title = "2.2.2.2 Display"
date = 2026-08-11T11:30:00+08:00
weight = 416
type = "docs"
description = "02-Display — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/display.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/display.html)

# 2.2.2.2 Display

“写入字符串” trait，优先考虑终端用户的可读性。

可派生：❌，除非使用 `derive_more` 之类 crate。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug)]
pub enum NetworkError {
    HttpCode(u16),
    WhaleBitTheUnderseaCable,
}

impl std::fmt::Display for NetworkError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            NetworkError::HttpCode(code) => write!(f, "HTTP Error code {code}"),
            NetworkError::WhaleBitTheUnderseaCable => {
                write!(f, "Whale attack detected – call Ishmael")
            }
        }
    }
}

fn main() {
    let http = NetworkError::HttpCode(404);
    let whale = NetworkError::WhaleBitTheUnderseaCable;

    println!("http debug: {:?}", http);
    println!("http display: {}", http);
    println!("whale debug: {:?}", whale);
    println!("whale display: {}", whale);
}
```

> - 类似 `Debug` 的 trait，但聚焦于终端用户可读性。
>
> - `Error` trait 的前置条件。若为错误类型实现，聚焦于为用户及除你以外的程序员提供描述性错误。
>
> - 与 Debug 有相同的安全考量：考虑敏感数据可能通过 UI 或日志暴露的方式。
>
> - 实现 `Display` 的类型会自动实现 `ToString`。
>
> - 比较我们示例错误类型上 `Debug` 与 `Display` 的行为。说明 `Debug` 实现更直接地表示代码中的数据形态，而 `Display` 为非程序员提供更友好的消息。

