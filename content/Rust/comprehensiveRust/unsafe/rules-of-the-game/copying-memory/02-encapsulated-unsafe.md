+++
title = "5.2.2 封装的 Unsafe Rust"
date = 2026-08-11T11:30:00+08:00
weight = 529
type = "docs"
description = "02-封装的 Unsafe Rust — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/copying-memory/encapsulated-unsafe.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/copying-memory/encapsulated-unsafe.html)

# 5.2.2 封装的 Unsafe Rust

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub fn copy(dest: &mut [u8], source: &[u8]) {
    let len = dest.len().min(source.len());
    let mut i = 0;
    while i < len {
        // SAFETY：`i` 必定在边界内，因为它由 source.len() 得出
        let new = unsafe { source.get_unchecked(i) };

        // SAFETY：`i` 必定在边界内，因为它由 dest.len() 得出
        let old = unsafe { dest.get_unchecked_mut(i) };

        *old = *new;
        i += 1;
    }
}

fn main() {
    let a = &[114, 117, 115, 116];
    let b = &mut [82, 85, 83, 84];

    println!("{}", String::from_utf8_lossy(b));
    copy(b, a);
    println!("{}", String::from_utf8_lossy(b));
}
```

> 「这里有一个安全函数，它在内部封装了 `unsafe` 块。
>
> 「该实现避开了迭代器，改由实现者手动访问内存。」
>
> 「这样正确吗？」「有没有问题？」
>
> 「谁负责保证正确性？函数作者。
>
> 「含 `unsafe` 块的安全函数，如果任何输入都不可能引发内存安全问题，则仍然健全。

