+++
title = "03-修改变量"
date = 2026-08-17T22:00:00+08:00
weight = 6
type = "docs"
description = "修改变量 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/04_zh-cn.html](https://tourofrust.com/04_zh-cn.html)

# 修改变量

Rust 非常关心哪些变量是可修改的。值分为两种类型：

* **可变的** - 编译器允许对变量进行读取和写入。
* **不可变的** - 编译器只允许对变量进行读取。

可变值用 **mut** 关键字表示。

关于这个概念，我们之后还会有更多的内容，但是眼下请谨记这个关键字即可。

## 示例代码

```rust
fn main() {
    let mut x = 42;
    println!("{}", x);
    x = 13;
    println!("{}", x);
}
```
