+++
title = "3.7 数据结构中的生命周期"
date = 2026-08-11T11:30:00+08:00
weight = 157
type = "docs"
description = "07-数据结构中的生命周期 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/lifetimes/struct-lifetimes.html](https://google.github.io/comprehensive-rust/lifetimes/struct-lifetimes.html)

# 3.7 数据结构中的生命周期

若数据类型存储借用的数据，必须用生命周期标注：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug)]
enum HighlightColor {
    Pink,
    Yellow,
}

#[derive(Debug)]
struct Highlight<'document> {
    slice: &'document str,
    color: HighlightColor,
}

fn main() {
    let doc = String::from("The quick brown fox jumps over the lazy dog.");
    let noun = Highlight { slice: &doc[16..19], color: HighlightColor::Yellow };
    let verb = Highlight { slice: &doc[20..25], color: HighlightColor::Pink };
    // drop(doc);
    dbg!(noun);
    dbg!(verb);
}
```

> - 在上面的例子中，`Highlight` 上的标注强制要求：被包含的 `&str` 所依赖的底层数据，至少要与任何使用该数据的 `Highlight` 实例活得一样长。结构体不能比它所引用的数据活得更久。
> - 若在 `noun` 或 `verb` 的生命周期结束之前丢弃 `doc`，借用检查器会报错。
> - 带有借用数据的类型会迫使用户持有原始数据。这对创建轻量视图很有用，但通常也使它们更难使用。
> - 可能的话，让数据结构直接拥有其数据。
> - 某些内部有多个引用的结构体可以有多个生命周期标注。若除了结构体自身的生命周期外，还需要描述引用之间的生命周期关系，这就可能是必要的。那些是非常高级的用例。

