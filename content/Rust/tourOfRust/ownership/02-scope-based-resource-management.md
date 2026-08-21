+++
title = "02-基于域的资源管理"
date = 2026-08-17T22:00:00+08:00
weight = 46
type = "docs"
description = "基于域的资源管理 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/44_zh-cn.html](https://tourofrust.com/44_zh-cn.html)

# 基于域的资源管理

Rust 将使用资源最后被使用的位置或者一个函数域的结束来作为资源被析构和释放的地方。 此处析构和释放的概念被称之为 **drop**（丢弃）。

内存细节：
* Rust 没有垃圾回收机制。
* 在 C++ 中，这被也称为“资源获取即初始化“（RAII）。

## 示例代码

```rust
struct Foo {
    x: i32,
}

fn main() {
    let foo_a = Foo { x: 42 };
    let foo_b = Foo { x: 13 };

    println!("{}", foo_a.x);
    // foo_a 将在这里被 dropped 因为其在这之后再也没有被使用

    println!("{}", foo_b.x);
    // foo_b 将在这里被 dropped 因为这是函数域的结尾
}
```
