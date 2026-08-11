+++
title = "5.2.5 狼来了"
date = 2026-08-11T11:30:00+08:00
weight = 532
type = "docs"
description = "05-狼来了 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/copying-memory/crying-wolf.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/copying-memory/crying-wolf.html)

# 5.2.5 狼来了

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub unsafe fn copy(dest: &mut [u8], source: &[u8]) {
    for (dest, src) in dest.iter_mut().zip(source) {
        *dest = *src;
    }
}

fn main() {
    let a = &[114, 117, 115, 116];
    let b = &mut [82, 85, 83, 84];

    println!("{}", String::from_utf8_lossy(b));
    unsafe { copy(b, a) };
    println!("{}", String::from_utf8_lossy(b));
}
```

> 「也可以创建所谓的『狼来了』函数。
>
> 「这类函数被标记为 `unsafe`，但程序员无需检查任何安全前置条件。

