+++
title = "2.2.1.8 From"
date = 2026-08-11T11:30:00+08:00
weight = 408
type = "docs"
description = "08-From — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/from.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/from.html)

# 2.2.1.8 From

构造函数，强烈暗示“类型转换”。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
impl Duration {
    fn from_days(days: u64) -> Duration;
}

impl i32 {
    fn from_ascii(src: &[u8]) -> Result<i32, ParseIntError>;
}

impl u32 {
    fn from_le_bytes(bytes: [u8; 4]) -> u32;
}
```

> - 构造风格、类似 `From` trait 的函数前缀。
>
> - 这些函数可接受多个参数，但通常暗示用户比普通构造函数做更多工作。
>
> - 对大多数构造风格函数仍偏好 `new`；`from` 的含义是把一种数据类型变换为另一种。

