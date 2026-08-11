+++
title = "3.1.2 强制不变量"
date = 2026-08-11T11:30:00+08:00
weight = 428
type = "docs"
description = "02-强制不变量 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/newtype-pattern/parse-don-t-validate.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/newtype-pattern/parse-don-t-validate.html)

# 3.1.2 强制不变量

可以利用 newtype 模式强制**不变量**（invariants）。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub struct Username(String);

impl Username {
    pub fn new(username: String) -> Result<Self, InvalidUsername> {
        if username.is_empty() {
            return Err(InvalidUsername::CannotBeEmpty)
        }
        if username.len() > 32 {
            return Err(InvalidUsername::TooLong { len: username.len() })
        }
        Ok(Self(username))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}
# pub enum InvalidUsername {
#     CannotBeEmpty,
#     TooLong { len: usize },
# }
```

> - Newtype 模式结合 Rust 的模块与可见性系统，可以**保证**某类型的实例满足一组不变量。
>
>   在上例中，`Username` 结构体内的原始 `String` 无法从其他模块或 crate 直接访问，因为它未标为 `pub` 或 `pub(in ...)`。`Username` 的使用者必须通过 `new` 方法创建实例。而 `new` 会执行校验，从而确保所有 `Username` 实例都满足这些检查。
>
> - `as_str` 方法允许使用者访问原始字符串表示（例如写入数据库）。但使用者不能修改底层值，因为返回类型 `&str` 限制为只读访问。
>
> - 类型级不变量还有二阶收益。
>
>   输入在边界处校验一次，程序其余部分可以依赖这些不变量始终成立。我们可以避免在程序各处做冗余校验和「防御性编程」检查，从而减少噪音并提升性能。

