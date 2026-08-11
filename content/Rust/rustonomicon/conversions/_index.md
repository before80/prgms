+++
title = "第4章 类型转换"
date = 2026-08-06T17:08:00+08:00
weight = 22
type = "docs"
description = "强制转换、点运算符、强制转型与 transmute"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 类型转换


> 原文链接: [https://doc.rust-lang.org/nomicon/conversions.html](https://doc.rust-lang.org/nomicon/conversions.html)


　　归根结底，一切不过是某处的一堆比特，类型系统只是帮我们把比特用对。对比特进行类型化有两个常见问题：需要把那些*完全相同的*比特重新解释为另一种类型，以及需要改变比特使其对另一种类型具有等价含义。由于 Rust 鼓励在类型系统中编码重要性质，这些问题极其普遍。因此 Rust 提供了多种解决方式。

　　首先看 Safe Rust 提供的重新解释值的方式。
　　最直接的方式是把值解构为组成部分，再用它们构造新类型。例如：

```rust
struct Foo {
    x: u32,
    y: u16,
}

struct Bar {
    a: u32,
    b: u16,
}

fn reinterpret(foo: Foo) -> Bar {
    let Foo { x, y } = foo;
    Bar { a: x, b: y }
}
```

　　但这充其量很烦人。对常见转换，Rust 提供了更符合人体工程学的替代方案。
