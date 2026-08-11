+++
title = "3.2 文档"
date = 2026-08-11T11:30:00+08:00
weight = 104
type = "docs"
description = "02-文档 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/std-types/docs.html](https://google.github.io/comprehensive-rust/std-types/docs.html)

# 3.2 文档

Rust 自带详尽文档。例如：

- 关于
  [循环](https://doc.rust-lang.org/stable/reference/expressions/loop-expr.html)
  的全部细节。
- 原始类型如
  [`u8`](https://doc.rust-lang.org/stable/std/primitive.u8.html)。
- 标准库类型如
  [`Option`](https://doc.rust-lang.org/stable/std/option/enum.Option.html) 或
  [`BinaryHeap`](https://doc.rust-lang.org/stable/std/collections/struct.BinaryHeap.html)。

用 `rustup doc --std` 或 <https://std.rs> 查看文档。

实际上，你也可以为自己的代码写文档：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 判断第一个参数是否能被第二个参数整除。
///
/// 若第二个参数为零，结果为 false。
fn is_divisible_by(lhs: u32, rhs: u32) -> bool {
    if rhs == 0 {
        return false;
    }
    lhs % rhs == 0
}
```

内容按 Markdown 处理。所有已发布的 Rust 库 crate 都会通过
[rustdoc](https://doc.rust-lang.org/rustdoc/what-is-rustdoc.html)
工具自动在 [`docs.rs`](https://docs.rs) 上生成文档。惯用做法是用这种模式为 API 中所有公开项写文档。

要从项内部（例如模块内部）为该项写文档，使用 `//!` 或 `/*! .. */`，称为「内部文档注释」：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
//! 本模块包含与整数整除相关的功能。
```

> - 向学员展示 `rand` crate 的生成文档：
>   <https://docs.rs/rand>。

