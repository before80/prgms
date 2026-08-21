+++
title = "01-`From` 和 `Into`"
date = 2026-08-20T21:20:00+08:00
weight = 32
type = "docs"
description = "`From` 和 `Into` — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/conversion/from_into.html](https://doc.rust-lang.org/stable/rust-by-example/conversion/from_into.html)

# `From` 和 `Into`

 [`From`] 和 [`Into`] 两个 trait 是内部相关联的，实际上这是它们实现的一部分。如果我们能够从类型 B 得到类型 A，那么很容易相信我们也能够把类型 A 转换为类型 B。

## `From` {#from}

[`From`] trait 允许一种类型定义 “怎么根据另一种类型生成自己”，因此它提供了一种类型转换的简单机制。在标准库中有无数 `From` 的实现，规定原生类型及其他常见类型的转换功能。

比如，可以很容易地把 `str` 转换成 `String`：

```rust
let my_str = "hello";
let my_string = String::from(my_str);
```
也可以为我们自己的类型定义转换机制：

```rust
use std::convert::From;

#[derive(Debug)]
struct Number {
    value: i32,
}

impl From<i32> for Number {
    fn from(item: i32) -> Self {
        Number { value: item }
    }
}

fn main() {
    let num = Number::from(30);
    println!("My number is {:?}", num);
}
```
## `Into` {#into}

[`Into`] trait 就是把 `From` trait 倒过来而已。也就是说，如果你为你的类型实现了 `From`，那么同时你也就免费获得了 `Into`。

使用 `Into` trait 通常要求指明要转换到的类型，因为编译器大多数时候不能推断它。不过考虑到我们免费获得了 `Into`，这点代价不值一提。

```rust
use std::convert::Into;

#[derive(Debug)]
struct Number {
    value: i32,
}

impl Into<Number> for i32 {
    fn into(self) -> Number {
        Number { value: self }
    }
}

fn main() {
    let int = 5;
    // 试试删除类型注释
    let num: Number = int.into();
    println!("My number is {:?}", num);
}
```
[`From`]: https://rustwiki.org/zh-CN/std/convert/trait.From.html
[`Into`]: https://rustwiki.org/zh-CN/std/convert/trait.Into.html
