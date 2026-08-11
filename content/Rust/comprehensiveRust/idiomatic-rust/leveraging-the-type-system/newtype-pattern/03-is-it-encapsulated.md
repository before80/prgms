+++
title = "3.1.3 真的封装了吗？"
date = 2026-08-11T11:30:00+08:00
weight = 429
type = "docs"
description = "03-真的封装了吗？ — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/newtype-pattern/is-it-encapsulated.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/newtype-pattern/is-it-encapsulated.html)

# 3.1.3 真的封装了吗？

你必须评估 newtype **暴露的整个 API 面**，才能判断不变量是否真的牢不可破。必须考虑所有可能的交互，包括可能让用户绕过校验的 trait 实现。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub struct Username(String);

impl Username {
    pub fn new(username: String) -> Result<Self, InvalidUsername> {
        // 校验检查...
        Ok(Self(username))
    }
}

impl std::ops::DerefMut for Username { // ‼️
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}
# impl std::ops::Deref for Username {
#     type Target = str;
#
#     fn deref(&self) -> &Self::Target {
#         &self.0
#     }
# }
# pub struct InvalidUsername;
```

> - `DerefMut` 允许用户取得对被包装值的可变引用。
>
>   该可变引用可被用于修改底层数据，从而可能破坏 `Username::new` 强制的不变量！
>
> - 审计 newtype 的 API 面时，可将审查范围收窄到提供对底层数据可变访问的方法和 trait。
>
> - 提醒学员注意隐私边界。
>
>   特别是，与 newtype 定义在同一模块中的函数和方法可以直接访问其底层数据。若可能，将 newtype 定义移到独立模块，以缩小审计范围。

