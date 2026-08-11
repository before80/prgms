+++
title = "4.3 编译器 Lint 与 Clippy"
date = 2026-08-11T11:30:00+08:00
weight = 181
type = "docs"
description = "03-编译器 Lint 与 Clippy — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/testing/lints.html](https://google.github.io/comprehensive-rust/testing/lints.html)

# 4.3 编译器 Lint 与 Clippy

Rust 编译器能给出出色的错误信息，以及有用的内置 lint。[Clippy](https://doc.rust-lang.org/clippy/) 提供更多 lint，并按组组织，可按项目启用。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[deny(clippy::cast_possible_truncation)]
fn main() {
    let mut x = 3;
    while (x < 70000) {
        x *= 2;
    }
    println!("X probably fits in a u16, right? {}", x as u16);
}
```

> 这里可以看到编译器 lint，但看不到 Clippy lint。在 playground 上运行 `clippy` 以展示 Clippy 警告。Clippy 对其 lint 有详尽文档，并且不断新增 lint（包括默认 deny 的 lint）。
>
> 注意：带有 `help: ...` 的错误或警告可以用 `cargo fix` 或通过编辑器自动修复。

