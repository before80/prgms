+++
title = "4.1.3 派生 Trait"
date = 2026-08-11T11:30:00+08:00
weight = 472
type = "docs"
description = "03-派生 Trait — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/deriving-traits.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/deriving-traits.html)

# 4.1.3 派生 Trait

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
struct BufferId([u8; 16]);

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
struct DrawingBuffer {
    target: [u8; 16],
    commands: Vec<String>,
}
```

> - 许多 trait、协议、接口都有平凡的实现，用机械方式写出来很容易。
>
> - 可以把类型定义（其语法树）交给过程宏（编译器插件），自动生成 trait 实现。
>
>   这些宏必须由人编写；编译器无法自行推断一切。
>
> - 许多 trait 都有朴素、显而易见的实现，大多依赖「所有字段或变体都已实现该 trait」。
>
>   若某类型的字段 / 变体都实现了 `PartialEq`/`Eq`，就可以相当容易地派生它们：逐一对齐字段 / 变体，任一不匹配则相等检查返回 false。
>
> - Derive 让我们能以机械、可预期的方式避免样板代码；derive 实现的作者通常也是该 trait 的作者，会按正确的语义来设计派生逻辑。
>
> - 向学员提问：你们是否处理过「大部分代码都是平凡样板」的代码库？
>
> - 这与 Haskell 的 `deriving` 系统类似。
>
> 参考：
>
> - https://doc.rust-lang.org/reference/attributes/derive.html#r-attributes.derive

