+++
title = "02-方法调用"
date = 2026-08-17T22:00:00+08:00
weight = 26
type = "docs"
description = "方法调用 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/24_zh-cn.html](https://tourofrust.com/24_zh-cn.html)

# 方法调用

与函数（function）不同，方法（method）是与特定数据类型关联的函数。

**静态方法** — 属于某个类型，调用时使用 `::` 运算符。

**实例方法** — 属于某个类型的实例，调用时使用 `.` 运算符。

我们将在后续章节中更多地讨论如何创建自己的方法。

## 示例代码

```rust
fn main() {
    // 使用静态方法来创建一个String实例
    let s = String::from("Hello world!");
    // 使用实例来调用方法
    println!("{} is {} characters long.", s, s.len());
}
```
