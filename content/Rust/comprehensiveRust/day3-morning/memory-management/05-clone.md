+++
title = "2.5 `Clone`"
date = 2026-08-11T11:30:00+08:00
weight = 128
type = "docs"
description = "05-`Clone` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/memory-management/clone.html](https://google.github.io/comprehensive-rust/memory-management/clone.html)

# 2.5 `Clone`

有时你_确实想要_拷贝一个值。`Clone` trait 就是为此准备的。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn say_hello(name: String) {
    println!("Hello {name}")
}

fn main() {
    let name = String::from("Alice");
    say_hello(name.clone());
    say_hello(name);
}
```

> - `Clone` 的用意是让堆分配发生的位置一目了然。请留意 `.clone()`，以及 `vec!`、`Box::new` 等少数其他位置。
>
> - 常见做法是先「用 clone 绕过」借用检查器问题，稍后再回来优化掉这些克隆。
>
> - `clone` 一般会做深拷贝：例如克隆数组时，数组的每个元素也会被克隆。
>
> - `clone` 的行为由用户定义，因此需要时可以实现自定义克隆逻辑。

