+++
title = "2.5.1 `if let` 表达式"
date = 2026-08-11T11:30:00+08:00
weight = 71
type = "docs"
description = "01-`if let` 表达式 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/pattern-matching/let-control-flow/if-let.html](https://google.github.io/comprehensive-rust/pattern-matching/let-control-flow/if-let.html)

# 2.5.1 `if let` 表达式

[`if let` 表达式](https://doc.rust-lang.org/reference/expressions/if-expr.html#if-let-expressions)
可以根据值是否匹配某个模式来执行不同代码：

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::time::Duration;

fn sleep_for(secs: f32) {
    let result = Duration::try_from_secs_f32(secs);

    if let Ok(duration) = result {
        std::thread::sleep(duration);
        println!("slept for {duration:?}");
    }
}

fn main() {
    sleep_for(-10.0);
    sleep_for(0.8);
}
```

> - 与 `match` 不同，`if let` 不必覆盖所有分支，因此有时比 `match` 更简洁。
> - 常见用法是处理 `Option` 中的 `Some` 值。
> - 与 `match` 不同，`if let` 不支持用于模式匹配的守卫子句。
> - 带上 `else` 子句时，它可以作为表达式使用。

