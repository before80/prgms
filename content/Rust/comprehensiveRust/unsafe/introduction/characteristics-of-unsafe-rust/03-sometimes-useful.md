+++
title = "3.5.3 有时很有用"
date = 2026-08-11T11:30:00+08:00
weight = 512
type = "docs"
description = "03-有时很有用 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/characteristics-of-unsafe-rust/sometimes-useful.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/characteristics-of-unsafe-rust/sometimes-useful.html)

# 3.5.3 有时很有用

你的代码可以跑得更快！

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn iter_sum(xs: &[u64]) -> u64 {
    xs.iter().sum()
}

fn fast_sum(xs: &[u64]) -> u64 {
    let mut acc = 0;
    let mut i = 0;
    unsafe {
        while i < xs.len() {
            acc += *xs.get_unchecked(i);
            i += 1;
        }
    }
    acc
}

fn main() {
    let data: Vec<_> = (0..1_000_000).collect();

    let baseline = iter_sum(&data);
    let unchecked = fast_sum(&data);

    assert_eq!(baseline, unchecked);
}
```

> 使用 `unsafe` 的代码 _可能_ 更快。
>
> `fast_sum()` 跳过了 bounds check（边界检查）。然而，要验证性能主张，必须进行 benchmark（基准测试）。对于这类情况，Rust 的 iterator（迭代器）通常也能消除边界检查。
>
> 可选：[展示两个函数生成的相同汇编][godbolt]。
>
> [godbolt]: https://rust.godbolt.org/z/d48v1Y5aj

