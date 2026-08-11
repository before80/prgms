+++
title = "4.5 常量"
date = 2026-08-11T11:30:00+08:00
weight = 59
type = "docs"
description = "05-常量 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/user-defined-types/const.html](https://google.github.io/comprehensive-rust/user-defined-types/const.html)

# 4.5 常量

常量在编译期求值，其值会在使用处被[内联][1]：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
const DIGEST_SIZE: usize = 3;
const FILL_VALUE: u8 = calculate_fill_value();

const fn calculate_fill_value() -> u8 {
    if DIGEST_SIZE < 10 { 42 } else { 13 }
}

fn compute_digest(text: &str) -> [u8; DIGEST_SIZE] {
    let mut digest = [FILL_VALUE; DIGEST_SIZE];
    for (idx, &b) in text.as_bytes().iter().enumerate() {
        digest[idx % DIGEST_SIZE] = digest[idx % DIGEST_SIZE].wrapping_add(b);
    }
    digest
}

fn main() {
    let digest = compute_digest("Hello");
    println!("digest: {digest:?}");
}
```

只有标记为 `const` 的函数才能在编译期被调用来生成 `const` 值。不过 `const` 函数也可以在运行时调用。

> - 可以提到：`const` 在语义上与 C++ 的 `constexpr` 类似


[1]: https://rust-lang.github.io/rfcs/0246-const-vs-static.html
