+++
title = "4.5 `break` 与 `continue`"
date = 2026-08-11T11:30:00+08:00
weight = 31
type = "docs"
description = "`break` 与 `continue` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/control-flow-basics/break-continue.html](https://google.github.io/comprehensive-rust/control-flow-basics/break-continue.html)

# 4.5 `break` 与 `continue`

若要立即开始下一次迭代，使用
[`continue`](https://doc.rust-lang.org/reference/expressions/loop-expr.html#continue-expressions)。

若要提前退出任意类型的循环，使用
[`break`](https://doc.rust-lang.org/reference/expressions/loop-expr.html#break-expressions)。
对 `loop` 而言，`break` 可以带一个可选表达式，该表达式会成为 `loop` 表达式的值。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let mut i = 0;
    loop {
        i += 1;
        if i > 5 {
            break;
        }
        if i % 2 == 0 {
            continue;
        }
        dbg!(i);
    }
}
```

> 注意：`loop` 是唯一能返回非平凡值的循环结构。这是因为它保证只在 `break` 语句处返回（与 `while` 和 `for` 循环不同，后两者还可能在条件失败时返回）。

