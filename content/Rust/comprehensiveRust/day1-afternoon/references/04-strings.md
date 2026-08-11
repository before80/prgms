+++
title = "3.4 字符串"
date = 2026-08-11T11:30:00+08:00
weight = 50
type = "docs"
description = "04-字符串 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/references/strings.html](https://google.github.io/comprehensive-rust/references/strings.html)

# 3.4 字符串

现在可以理解 Rust 中的两种字符串类型了：

- `&str` 是 UTF-8 编码字节的切片，类似 `&[u8]`。
- `String` 是拥有所有权的 UTF-8 编码字节缓冲区，类似 `Vec<T>`。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let s1: &str = "World";
    println!("s1: {s1}");

    let mut s2: String = String::from("Hello ");
    println!("s2: {s2}");

    s2.push_str(s1);
    println!("s2: {s2}");

    let s3: &str = &s2[2..9];
    println!("s3: {s3}");
}
```

> - `&str` 引入字符串切片：对存储在某块内存中的 UTF-8 编码字符串数据的不可变引用。字符串字面量（`"Hello"`）存放在程序的二进制中。
>
> - Rust 的 `String` 类型是字节向量的包装。与 `Vec<T>` 一样，它拥有所有权。
>
> - 与许多其他类型一样，`String::from()` 从字符串字面量创建字符串；`String::new()` 创建空字符串，之后可用 `push()` 和 `push_str()` 追加数据。
>
> - `format!()` 宏是从动态值生成拥有所有权的字符串的便捷方式。它接受与 `println!()` 相同的格式说明。
>
> - 可以通过 `&` 以及可选的范围选择从 `String` 借用 `&str` 切片。若选择的字节范围未对齐到字符边界，表达式会 panic。`chars` 迭代器按字符遍历，比自己对齐字符边界更可取。
>
> - 对 C++ 程序员：可以把 `&str` 想成 C++ 的 `std::string_view`，但它总是指向内存中有效的字符串。Rust 的 `String` 大致相当于 C++ 的 `std::string`（主要区别：它只能包含 UTF-8 编码字节，且从不使用小字符串优化）。
>
> - 字节字符串字面量可以直接创建 `&[u8]` 值：
>
>     ```rust
>   // Copyright 2024 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   fn main() {
>       println!("{:?}", b"abc");
>       println!("{:?}", &[97, 98, 99]);
>   }
>   ```
>
> - 原始字符串允许创建禁用转义的 `&str` 值：`r"\n" == "\\n"`。可以在引号两侧使用相同数量的 `#` 来嵌入双引号：
>
>     ```rust
>   // Copyright 2024 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   fn main() {
>       println!(r#"<a href="link.html">link</a>"#);
>       println!("<a href=\"link.html\">link</a>");
>   }
>   ```

