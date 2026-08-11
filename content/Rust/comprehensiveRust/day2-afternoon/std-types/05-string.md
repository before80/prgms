+++
title = "3.5 `String`"
date = 2026-08-11T11:30:00+08:00
weight = 107
type = "docs"
description = "05-`String` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/std-types/string.html](https://google.github.io/comprehensive-rust/std-types/string.html)

# 3.5 `String`

[`String`][1] 是可增长的 UTF-8 编码字符串：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let mut s1 = String::new();
    s1.push_str("Hello");
    println!("s1: len = {}, capacity = {}", s1.len(), s1.capacity());

    let mut s2 = String::with_capacity(s1.len() + 1);
    s2.push_str(&s1);
    s2.push('!');
    println!("s2: len = {}, capacity = {}", s2.len(), s2.capacity());

    let s3 = String::from("🇨🇭");
    println!("s3: len = {}, number of chars = {}", s3.len(), s3.chars().count());
}
```

`String` 实现了 [`Deref<Target = str>`][2]，这意味着你可以在 `String` 上调用所有 `str` 方法。

[1]: https://doc.rust-lang.org/std/string/struct.String.html
[2]: https://doc.rust-lang.org/std/string/struct.String.html#deref-methods-str

> - `String::new` 返回新的空字符串；若知道要推入多少数据，用 `String::with_capacity`。
> - `String::len` 返回 `String` 的字节大小（可能与字符长度不同）。
> - `String::chars` 返回遍历实际字符的迭代器。注意：由于
>   [字形簇（grapheme clusters）](https://docs.rs/unicode-segmentation/latest/unicode_segmentation/struct.Graphemes.html)，
>   `char` 可能与人类认为的「字符」不同。
> - 人们说「字符串」时，可能指 `&str` 或 `String`。
> - 当类型实现 `Deref<Target = T>` 时，编译器会让你透明地调用 `T` 的方法。
>   - 我们还没讨论 `Deref` trait，因此此时这主要解释了文档侧栏的结构。
>   - `String` 实现了 `Deref<Target = str>`，从而透明地获得对 `str` 方法的访问。
>   - 写并比较 `let s3 = s1.deref();` 与 `let s3 = &*s1;`。
> - `String` 实现为字节向量的包装；你在向量上看到的许多操作在 `String` 上也支持，但带有一些额外保证。
> - 比较索引 `String` 的不同方式：
>   - 用 `s3.chars().nth(i).unwrap()` 取字符，其中 `i` 分别在界内、界外。
>   - 用 `s3[0..4]` 取子串，其中切片分别落在或不落在字符边界上。
> - 许多类型可用
>   [`to_string`](https://doc.rust-lang.org/std/string/trait.ToString.html#tymethod.to_string)
>   方法转成字符串。该 trait 会为所有实现了 `Display` 的类型自动实现，因此任何可格式化的东西也都能转成字符串。

