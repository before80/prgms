+++
title = "3.4 联合体"
date = 2026-08-11T11:30:00+08:00
weight = 200
type = "docs"
description = "04-联合体 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-rust/unions.html](https://google.github.io/comprehensive-rust/unsafe-rust/unions.html)

# 3.4 联合体

联合体（union）类似枚举（enum），但你需要自己跟踪当前活动字段：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[repr(C)]
union MyUnion {
    i: u8,
    b: bool,
}

fn main() {
    let u = MyUnion { i: 42 };
    println!("int: {}", unsafe { u.i });
    println!("bool: {}", unsafe { u.b }); // 未定义行为！
}
```

> <summary>讲师备注</summary>
>
> 在 Rust 中很少需要联合体，因为枚举是更优的替代方案。偶尔在与 C 库 API 交互时会需要它们。
>
> 若只是想把字节重新解释为另一种类型，你多半想用
> [`std::mem::transmute`](https://doc.rust-lang.org/stable/std/mem/fn.transmute.html)
> 或诸如 [`zerocopy`](https://crates.io/crates/zerocopy) 这样的安全封装。

