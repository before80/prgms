+++
title = "02-C 风格用法"
date = 2026-08-20T21:20:00+08:00
weight = 18
type = "docs"
description = "C 风格用法 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/custom_types/enum/c_like.html](https://doc.rust-lang.org/stable/rust-by-example/custom_types/enum/c_like.html)

# C 风格用法

`enum` 也可以像 C 语言风格的枚举类型那样使用。

```rust
// 该属性用于隐藏对未使用代码的警告。
#![allow(dead_code)]

// 拥有隐式辨别值（implicit discriminator，从 0 开始）的 enum
enum Number {
    Zero,
    One,
    Two,
}

// 拥有显式辨别值（explicit discriminator）的 enum
enum Color {
    Red = 0xff0000,
    Green = 0x00ff00,
    Blue = 0x0000ff,
}

fn main() {
    // `enum` 可以转成整型。
    println!("zero is {}", Number::Zero as i32);
    println!("one is {}", Number::One as i32);

    println!("roses are #{:06x}", Color::Red as i32);
    println!("violets are #{:06x}", Color::Blue as i32);
}
```
### 参考： {#参考}

[类型转换][cast]

[cast]: ../../types/01-cast/