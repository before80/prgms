+++
title = "4.3 `From` 与 `Into`"
date = 2026-08-11T11:30:00+08:00
weight = 115
type = "docs"
description = "03-`From` 与 `Into` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/std-traits/from-and-into.html](https://google.github.io/comprehensive-rust/std-traits/from-and-into.html)

# 4.3 `From` 与 `Into`

类型实现 [`From`][1] 与 [`Into`][2] 以便于类型转换。与 `as` 不同，这些 trait 对应无损、不可失败的转换。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let s = String::from("hello");
    let addr = std::net::Ipv4Addr::from([127, 0, 0, 1]);
    let one = i16::from(true);
    let bigger = i32::from(123_i16);
    println!("{s}, {addr}, {one}, {bigger}");
}
```

实现了 [`From`][1] 时，会自动实现 [`Into`][2]：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let s: String = "hello".into();
    let addr: std::net::Ipv4Addr = [127, 0, 0, 1].into();
    let one: i16 = true.into();
    let bigger: i32 = 123_i16.into();
    println!("{s}, {addr}, {one}, {bigger}");
}
```

> - 因此通常只实现 `From`，类型也会自动获得 `Into` 实现。
> - 声明函数参数输入类型为「任何可转换成 `String` 的东西」时，规则相反：应使用 `Into`。你的函数会接受实现了 `From` 的类型，以及_只_实现了 `Into` 的类型。


[1]: https://doc.rust-lang.org/std/convert/trait.From.html
[2]: https://doc.rust-lang.org/std/convert/trait.Into.html
