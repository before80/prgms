+++
title = "2.3 借用错误"
date = 2026-08-11T11:30:00+08:00
weight = 144
type = "docs"
description = "03-借用错误 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/borrowing/examples.html](https://google.github.io/comprehensive-rust/borrowing/examples.html)

# 2.3 借用错误

作为这些借用规则如何防止内存错误的具体例子，考虑在仍有对集合元素的引用时修改集合的情况：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let mut vec = vec![1, 2, 3, 4, 5];
    let elem = &vec[2];
    vec.push(6);
    dbg!(elem);
}
```

类似地，考虑迭代器失效的情况：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let mut vec = vec![1, 2, 3, 4, 5];
    for elem in &vec {
        vec.push(elem * 2);
    }
}
```

> - 在这两种情况下，通过向集合推入新元素来修改它，若集合需要重新分配，都可能使已有的对集合元素的引用失效。

