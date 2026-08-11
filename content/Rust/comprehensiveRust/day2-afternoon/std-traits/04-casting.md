+++
title = "4.4 强制转换"
date = 2026-08-11T11:30:00+08:00
weight = 116
type = "docs"
description = "04-强制转换 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/std-traits/casting.html](https://google.github.io/comprehensive-rust/std-traits/casting.html)

# 4.4 强制转换

Rust 没有_隐式_类型转换，但支持用 `as` 做显式强制转换。在 C 语义有定义的地方，它们通常遵循 C 语义。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let value: i64 = 1000;
    println!("as u16: {}", value as u16);
    println!("as i16: {}", value as i16);
    println!("as u8: {}", value as u8);
}
```

`as` 的结果在 Rust 中_总是_有定义，且跨平台一致。这可能与你对改符号或转到更小类型的直觉不符——请查阅文档，并加注释说明意图。

用 `as` 做强制转换是一把相对锋利的工具，容易用错，也可能在后续维护改变所用类型或类型中的取值范围时成为微妙 bug 的来源。最好只在意图是「无条件截断」时使用（例如用 `as u32` 取 `u64` 的低 32 位，不论高位是什么）。

对于不可失败的转换（例如 `u32` 到 `u64`），优先用 `From` 或 `Into` 而不是 `as`，以确认转换确实不可失败。对于可失败的转换，当你想区别处理「能放下」与「放不下」的情况时，可用 `TryFrom` 与 `TryInto`。

> 讲完本页后可考虑休息一下。
>
> `as` 类似 C++ 的 static cast。在可能丢数据的情况下使用 `as` 一般不推荐，或至少应加解释性注释。
>
> 把整数强制转换成 `usize` 以作索引时，这种情况很常见。

