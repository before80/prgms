+++
title = "2.2.2.9 TryFrom 与 TryInto"
date = 2026-08-11T11:30:00+08:00
weight = 423
type = "docs"
description = "09-TryFrom 与 TryInto — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/try-from-into.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/try-from-into.html)

# 2.2.2.9 TryFrom 与 TryInto

从一种类型到另一种类型的可失败转换。

可派生：❌

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug)]
pub struct InvalidNumber;

#[derive(Debug)]
pub struct DivisibleByTwo(usize);

impl TryFrom<usize> for DivisibleByTwo {
    type Error = InvalidNumber;

    fn try_from(value: usize) -> Result<Self, InvalidNumber> {
        if value.rem_euclid(2) == 0 {
            Ok(DivisibleByTwo(value))
        } else {
            Err(InvalidNumber)
        }
    }
}

fn main() {
    let success: Result<DivisibleByTwo, _> = 4.try_into();
    dbg!(success);
    let fail: Result<DivisibleByTwo, _> = 5.try_into();
    dbg!(fail);
}
```

> - 提供可能失败的转换，返回 result 类型。
>
> - 与 `From`/`Into` 一样，优先为类型实现 `TryFrom` 而非 `TryInto`。
>
> - 实现可指定 `Result` 的错误类型。

