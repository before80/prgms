+++
title = "2.2.1.6 With：闭包"
date = 2026-08-11T11:30:00+08:00
weight = 406
type = "docs"
description = "06-With：闭包 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/with-closure.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/with-closure.html)

# 2.2.1.6 With：闭包

`with` 意为“做 X，但用这种特定方式计算。”

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
impl<T> Vec<T> {
    // 简化。若 resize 大于当前 vec 大小，用闭包填充元素。
    pub fn resize_with(&mut self, new_len: usize, f: impl FnMut() -> T);
}

mod iter {
    // 用闭包创建无限、惰性迭代器。
    pub fn repeat_with<A, F: FnMut() -> A>(repeater: F) -> RepeatWith<F>;
}
```

> - `with` 可作为后缀出现，表示可用某个特定函数或闭包，代替计算的“合理默认”。
>
>   类似于 [`by`](./12-by.md)。

