+++
title = "4.4 类型别名"
date = 2026-08-11T11:30:00+08:00
weight = 58
type = "docs"
description = "04-类型别名 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/user-defined-types/aliases.html](https://google.github.io/comprehensive-rust/user-defined-types/aliases.html)

# 4.4 类型别名

类型别名（type alias）为另一类型创建名称。这两种类型可以互换使用。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
enum CarryableConcreteItem {
    Left,
    Right,
}

type Item = CarryableConcreteItem;

// 别名在处理又长又复杂的类型时更有用：
use std::cell::RefCell;
use std::sync::{Arc, RwLock};
type PlayerInventory = RwLock<Vec<Arc<RefCell<Item>>>>;
```

> - [Newtype](tuple-structs.html) 往往是更好的选择，因为它会创建不同的类型。优先使用 `struct InventoryCount(usize)`，而不是
>   `type InventoryCount = usize`。
>
> - C 程序员会认出这与 `typedef` 类似。

