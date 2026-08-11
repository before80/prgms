+++
title = "4.1 比较"
date = 2026-08-11T11:30:00+08:00
weight = 113
type = "docs"
description = "01-比较 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/std-traits/comparisons.html](https://google.github.io/comprehensive-rust/std-traits/comparisons.html)

# 4.1 比较

这些 trait 支持值之间的比较。若类型的字段都实现了这些 trait，则可为该类型派生它们。

## `PartialEq` 与 `Eq`

`PartialEq` 是偏等价关系，必需方法是 `eq`，并提供方法 `ne`。`==` 与 `!=` 运算符会调用这些方法。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
struct Key {
    id: u32,
    metadata: Option<String>,
}
impl PartialEq for Key {
    fn eq(&self, other: &Self) -> bool {
        self.id == other.id
    }
}
```

`Eq` 是全等价关系（自反、对称、传递），并蕴含 `PartialEq`。需要全等价的函数会用 `Eq` 作为 trait 约束。

## `PartialOrd` 与 `Ord`

`PartialOrd` 定义偏序，带有 `partial_cmp` 方法。它用于实现 `<`、`<=`、`>=` 与 `>` 运算符。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::cmp::Ordering;
#[derive(Eq, PartialEq)]
struct Citation {
    author: String,
    year: u32,
}
impl PartialOrd for Citation {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        match self.author.partial_cmp(&other.author) {
            Some(Ordering::Equal) => self.year.partial_cmp(&other.year),
            author_ord => author_ord,
        }
    }
}
```

`Ord` 是全序，`cmp` 返回 `Ordering`。

> - `PartialEq` 可以在不同类型之间实现，但 `Eq` 不行，因为它是自反的：
>
>   ```rust
>   // Copyright 2023 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   struct Key {
>       id: u32,
>       metadata: Option<String>,
>   }
>   impl PartialEq<u32> for Key {
>       fn eq(&self, other: &u32) -> bool {
>           self.id == *other
>       }
>   }
>   ```
>
> - 实践中，派生这些 trait 很常见，手动实现则不常见。
>
> - 在 Rust 中比较引用时，比较的是所指对象的值，而不是引用本身。这意味着指向两个不同对象的引用，只要所指值相同，就可以比较为相等：
>
>   ```rust
>   // Copyright 2023 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   fn main() {
>       let a = "Hello";
>       let b = String::from("Hello");
>       assert_eq!(a, b);
>   }
>   ```

