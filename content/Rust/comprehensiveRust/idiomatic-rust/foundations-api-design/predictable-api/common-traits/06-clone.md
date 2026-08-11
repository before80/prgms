+++
title = "2.2.2.6 Clone"
date = 2026-08-11T11:30:00+08:00
weight = 420
type = "docs"
description = "06-Clone — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/clone.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/clone.html)

# 2.2.2.6 Clone

深拷贝类型，或复制可共享的智能指针。

可派生：✅

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::collections::BTreeSet;
use std::rc::Rc;

#[derive(Clone)]
pub struct LotsOfData {
    string: String,
    vec: Vec<u8>,
    set: BTreeSet<u8>,
}

fn main() {
    let lots_of_data = LotsOfData {
        string: "String".to_string(),
        vec: vec![1; 255],
        set: BTreeSet::from_iter([1, 2, 3, 4, 5, 6, 7, 8]),
    };

    // 深拷贝 `lots_of_data` 中的所有数据。
    let lots_of_data_cloned = lots_of_data.clone();

    let reference_counted = Rc::new(lots_of_data);

    // 复制引用计数指针，而非值本身。
    let reference_copied = reference_counted.clone();
}
```

> - “深拷贝”一个值；或在 `Rc`/`Arc` 这类引用计数指针的情况下，创建该指针的新实例。
>
> - 何时不要实现/派生：对那些为维护不变量而不应被复制的类型。我们稍后在地道 Rust 中会再谈。

