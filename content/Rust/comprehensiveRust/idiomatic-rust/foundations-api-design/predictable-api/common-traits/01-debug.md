+++
title = "2.2.2.1 Debug"
date = 2026-08-11T11:30:00+08:00
weight = 415
type = "docs"
description = "01-Debug — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/debug.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/debug.html)

# 2.2.2.1 Debug

用于调试目的的“写入字符串” trait。

可派生：✅

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug)]
pub struct Date {
    day: u8,
    month: u8,
    year: i64,
}

#[derive(Debug)]
pub struct User {
    name: String,
    date_of_birth: Date,
}

pub struct PlainTextPassword {
    password: String,
    hint: String,
}

impl std::fmt::Debug for PlainTextPassword {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("PlainTextPassword")
            .field("hint", &self.hint)
            .field("password", &"[omitted]")
            .finish()
    }
}

fn main() {
    let user = User {
        name: "Alice".to_string(),
        date_of_birth: Date { day: 31, month: 10, year: 2002 },
    };

    println!("{user:?}");
    println!(
        "{:?}",
        PlainTextPassword {
            password: "Password123".to_string(),
            hint: "Used it for years".to_string()
        }
    );
}
```

> - 提供平凡的“写入字符串”功能。
>
> - 为开发期间程序员提供*调试信息*的格式化，而非外观或序列化。
>
> - 允许在字符串格式化宏中使用 `{:?}` 与 `{#?}` 插值。
>
> - 何时不要派生/实现：若结构体持有敏感数据，调查是否应为它实现 `Debug`。
>
>   - 若需要 `Debug`，考虑手动实现而非派生。在实现中省略敏感数据。

