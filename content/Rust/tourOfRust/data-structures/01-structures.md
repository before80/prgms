+++
title = "01-结构体"
date = 2026-08-17T22:00:00+08:00
weight = 25
type = "docs"
description = "结构体 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/23_zh-cn.html](https://tourofrust.com/23_zh-cn.html)

# 结构体

一个 `struct` 就是一些字段的集合。

*字段*是一个与数据结构相关联的数据值。它的值可以是基本类型或结构体类型。

它的定义就像给编译器的蓝图，告诉编译器如何在内存中布局彼此相邻的字段。

## 示例代码

```rust
struct SeaCreature {
    // String 是个结构体
    animal_type: String,
    name: String,
    arms: i32,
    legs: i32,
    weapon: String,
}
```
