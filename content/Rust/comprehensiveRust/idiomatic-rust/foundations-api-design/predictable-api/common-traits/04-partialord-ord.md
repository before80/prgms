+++
title = "2.2.2.4 PartialOrd 与 Ord"
date = 2026-08-11T11:30:00+08:00
weight = 418
type = "docs"
description = "04-PartialOrd 与 Ord — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/partialord-ord.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/partialord-ord.html)

# 2.2.2.4 PartialOrd 与 Ord

偏序（partial ordering）与全序（total ordering）。

可派生：✅

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(PartialEq, PartialOrd)]
pub struct Partially(f32);

#[derive(PartialEq, Eq, PartialOrd, Ord)]
pub struct Totally {
    id: u32,
    name: String,
}

fn main() {
    let a = Totally { id: 0, name: "alice".into() };
    let b = Totally { id: 1, name: "alice".into() };
    let c = Totally { id: 0, name: "charlie".into() };

    dbg!(a.cmp(&b));
    dbg!(a.cmp(&c));
}
```

> - 与比较相关的方法。若类型实现了 `PartialOrd`/`Ord`，则可用比较运算符（`<`、`<=`、`>`、`>=`）。
>
> - `Ord` 提供 `min`、`max` 与 `clamp` 方法。
>
> - 派生时，按定义顺序比较。
>
>   对 enum，这意味着按书写顺序，每个变体被认为“大于”前一个。
>
>   对 struct，这意味着按书写顺序比较字段，因此在 `Totally` 中先比较 `id` 再比较 `name`。
>
> - 前置条件：`PartialOrd` 需要 `PartialEq`，`Ord` 需要 `Eq`。
>
>   要实现 `Ord`，类型还必须实现 `PartialEq`、`Eq` 与 `PartialOrd`。
>
> - 与 `PartialEq` 和 `Eq` 一样，类型若不实现 `PartialOrd`，就不能实现 `Ord`。
>
>   与那些相等性 trait 一样，`PartialOrd` 的存在是为了把具有非全序的类型（尤其是浮点数）与具有全序的类型分开。
>
> - 用于排序/搜索算法，以及维护 `BTreeMap`/`BTreeSet` 风格数据类型的顺序。

