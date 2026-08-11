+++
title = "4.4.2 `loop` 循环"
date = 2026-08-11T11:30:00+08:00
weight = 30
type = "docs"
description = "02-`loop` 循环 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/control-flow-basics/loops/loop.html](https://google.github.io/comprehensive-rust/control-flow-basics/loops/loop.html)

# 4.4.2 `loop` 循环

[`loop` 语句](https://doc.rust-lang.org/std/keyword.loop.html) 会一直循环，直到遇到 `break`。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let mut i = 0;
    loop {
        i += 1;
        dbg!(i);
        if i > 100 {
            break;
        }
    }
}
```

> - `loop` 语句的行为类似 `while true` 循环。适用于像服务器这样会永久提供连接的场景。

