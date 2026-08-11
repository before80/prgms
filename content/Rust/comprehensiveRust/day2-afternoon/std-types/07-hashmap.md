+++
title = "3.7 `HashMap`"
date = 2026-08-11T11:30:00+08:00
weight = 109
type = "docs"
description = "07-`HashMap` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/std-types/hashmap.html](https://google.github.io/comprehensive-rust/std-types/hashmap.html)

# 3.7 `HashMap`

带 HashDoS 攻击防护的标准哈希映射：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::collections::HashMap;

fn main() {
    let mut page_counts = HashMap::new();
    page_counts.insert("Adventures of Huckleberry Finn", 207);
    page_counts.insert("Grimms' Fairy Tales", 751);
    page_counts.insert("Pride and Prejudice", 303);

    if !page_counts.contains_key("Les Misérables") {
        println!(
            "We know about {} books, but not Les Misérables.",
            page_counts.len()
        );
    }

    for book in ["Pride and Prejudice", "Alice's Adventure in Wonderland"] {
        match page_counts.get(book) {
            Some(count) => println!("{book}: {count} pages"),
            None => println!("{book} is unknown."),
        }
    }

    // 用 .entry() 方法在找不到时插入值。
    for book in ["Pride and Prejudice", "Alice's Adventure in Wonderland"] {
        let page_count: &mut i32 = page_counts.entry(book).or_insert(0);
        *page_count += 1;
    }

    dbg!(page_counts);
}
```

> - `HashMap` 不在 prelude 中，需要引入作用域。
> - 试一下下面几行代码。第一行会查看书是否在哈希映射中，若不在则返回替代值。第二行会在找不到该书时把替代值插入哈希映射。
>
>   ```rust
>   // Copyright 2023 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   let pc1 = page_counts
>       .get("Harry Potter and the Sorcerer's Stone")
>       .unwrap_or(&336);
>   let pc2 = page_counts
>       .entry("The Hunger Games")
>       .or_insert(374);
>   ```
> - 与 `vec!` 不同，遗憾的是没有标准的 `hashmap!` 宏。
>   - 不过自 Rust 1.56 起，HashMap 实现了 [`From<[(K, V); N]>`][1]，
>     这让我们可以轻松从字面量数组初始化哈希映射：
>
>     ```rust
>     // Copyright 2023 Google LLC
>     // SPDX-License-Identifier: Apache-2.0
>     #
>     let page_counts = HashMap::from([
>       ("Harry Potter and the Sorcerer's Stone".to_string(), 336),
>       ("The Hunger Games".to_string(), 374),
>     ]);
>     ```
>
> - 或者，HashMap 可以从任何产生键值元组的 `Iterator` 构建。
>
> - 该类型有若干「方法专用」的返回类型，例如 `std::collections::hash_map::Keys`。搜索 Rust 文档时这些类型经常出现。向学员展示该类型的文档，以及返回到 `keys` 方法的有用链接。
>
> [1]: https://doc.rust-lang.org/std/collections/hash_map/struct.HashMap.html#impl-From%3C%5B(K,+V);+N%5D%3E-for-HashMap%3CK,+V,+RandomState%3E

