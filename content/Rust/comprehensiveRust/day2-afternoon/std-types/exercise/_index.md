+++
title = "3.8 练习：计数器"
date = 2026-08-11T11:30:00+08:00
weight = 110
type = "docs"
description = "练习：计数器 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/std-types/exercise.html](https://google.github.io/comprehensive-rust/std-types/exercise.html)

# 3.8 练习：计数器

在本练习中，你将取一个非常简单的数据结构并把它泛型化。它用
[`std::collections::HashMap`](https://doc.rust-lang.org/stable/std/collections/struct.HashMap.html)
跟踪见过哪些值，以及每个值出现了多少次。

`Counter` 的初始版本硬编码为只适用于 `u32` 值。让结构体及其方法对所跟踪的值类型泛型化，这样 `Counter` 就能跟踪任意类型的值。

若提前完成，试着用
[`entry`](https://doc.rust-lang.org/stable/std/collections/struct.HashMap.html#method.entry)
方法，把实现 `count` 所需的哈希查找次数减半。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::collections::HashMap;

/// Counter 统计类型 T 的每个值被见到的次数。
struct Counter {
    values: HashMap<u32, u64>,
}

impl Counter {
    /// 创建一个新的 Counter。
    fn new() -> Self {
        Counter {
            values: HashMap::new(),
        }
    }

    /// 对给定值计一次出现。
    fn count(&mut self, value: u32) {
        if self.values.contains_key(&value) {
            *self.values.get_mut(&value).unwrap() += 1;
        } else {
            self.values.insert(value, 1);
        }
    }

    /// 返回给定值已被见到的次数。
    fn times_seen(&self, value: u32) -> u64 {
        self.values.get(&value).copied().unwrap_or_default()
    }
}

fn main() {
    let mut ctr = Counter::new();
    ctr.count(13);
    ctr.count(14);
    ctr.count(16);
    ctr.count(14);
    ctr.count(14);
    ctr.count(11);

    for i in 10..20 {
        println!("saw {} values equal to {}", ctr.times_seen(i), i);
    }

    let mut strctr = Counter::new();
    strctr.count("apple");
    strctr.count("orange");
    strctr.count("apple");
    println!("got {} apples", strctr.times_seen("apple"));
}
```
