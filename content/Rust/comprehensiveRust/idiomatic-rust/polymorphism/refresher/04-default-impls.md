+++
title = "4.1.4 默认实现"
date = 2026-08-11T11:30:00+08:00
weight = 473
type = "docs"
description = "04-默认实现 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/default-impls.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/default-impls.html)

# 4.1.4 默认实现

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub trait CollectLeaves {
    type Leaf;

    // 必需方法
    fn collect_leaves_buffered(&self, buf: &mut Vec<Self::Leaf>);

    // 默认实现
    fn collect_leaves(&self) -> Vec<Self::Leaf> {
        let mut buf = vec![];
        self.collect_leaves_buffered(&mut buf);
        buf
    }
}
```

> - Trait 常有一些方法：只要你实现了必需方法，其余就会替你实现好。
>
> - 若方法体已写好，该 trait 方法就有默认实现。实现可以借助其它可用方法，例如同一 trait 的其它方法，或父 trait（supertrait）的方法。
>
> - 常见模式是：提供必须实现的核心功能（如 `Ord` 的 `compare`），再为可据此实现的函数给出默认实现（如 `Ord` 的 `max`/`min`/`clamp`）。
>
> - 默认方法可被 derive 宏覆盖，因为 derive 宏会在实现中生成任意 AST。
>
> 参考：
>
> - https://doc.rust-lang.org/reference/items/traits.html#r-items.traits.associated-item-decls

