+++
title = "3.8.1 解答"
date = 2026-08-11T11:30:00+08:00
weight = 111
type = "docs"
description = "01-解答 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/std-types/solution.html](https://google.github.io/comprehensive-rust/std-types/solution.html)

# 3.8.1 解答

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::collections::HashMap;
use std::hash::Hash;

/// Counter 统计类型 T 的每个值被见到的次数。
struct Counter<T> {
    values: HashMap<T, u64>,
}

impl<T: Eq + Hash> Counter<T> {
    /// 创建一个新的 Counter。
    fn new() -> Self {
        Counter { values: HashMap::new() }
    }

    /// 对给定值计一次出现。
    fn count(&mut self, value: T) {
        *self.values.entry(value).or_default() += 1;
    }

    /// 返回给定值已被见到的次数。
    fn times_seen(&self, value: T) -> u64 {
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
