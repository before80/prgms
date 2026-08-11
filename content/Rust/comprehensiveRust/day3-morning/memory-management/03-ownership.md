+++
title = "2.3 所有权"
date = 2026-08-11T11:30:00+08:00
weight = 126
type = "docs"
description = "03-所有权 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/memory-management/ownership.html](https://google.github.io/comprehensive-rust/memory-management/ownership.html)

# 2.3 所有权

所有变量绑定都有一个有效的作用域（scope）；在作用域外使用变量是错误：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
struct Point(i32, i32);

fn main() {
    {
        let p = Point(3, 4);
        dbg!(p.0);
    }
    dbg!(p.1);
}
```

我们说变量_拥有_（owns）该值。每个 Rust 值在任意时刻都恰好有一个所有者。

作用域结束时，变量被_丢弃_（dropped），数据被释放。此处可以运行析构函数以释放资源。

> 熟悉垃圾回收实现的学员会知道，GC 从一组「根」出发查找所有可达内存。Rust 的「单一所有者」原则是类似的思想。

