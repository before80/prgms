+++
title = "2.2.2.3 PartialEq 与 Eq"
date = 2026-08-11T11:30:00+08:00
weight = 417
type = "docs"
description = "03-PartialEq 与 Eq — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/partialeq-eq.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/partialeq-eq.html)

# 2.2.2.3 PartialEq 与 Eq

偏等（partial equality）与全等（total equality）。

可派生：✅

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(PartialEq, Eq)]
pub struct User { name: String, favorite_number: i32 }

fn main() {
    let alice = User { name: "alice".to_string(), favorite_number: 1_000_042 };
    let bob = User { name: "bob".to_string(), favorite_number: 42 };

    dbg!(alice == alice);
    dbg!(alice == bob);
}
```

> - 与相等性相关的方法。若类型实现了 `PartialEq`，则可用 `==`/`!=` 运算符。
>
> - 类型若不实现 `PartialEq`，就不能实现 `Eq`。
>
> - 提醒：偏（Partial）意味着“该集合中有对该函数无效的成员。”
>
>   这并不意味着相等会 panic，或返回 result，只是可能有些值的相等行为不如你所预期。
>
>   例如，浮点值中 `NaN` 是离群点：`NaN == NaN` 为 false，尽管按位相等。
>
>   `PartialEq` 的存在是为了把 `f32`/`f64` 这类类型与具有全等的类型分开。
>
> - 你可以在不同类型之间实现 `PartialEq`，但这大多对引用/智能指针类型有用。

