+++
title = "08-解引用"
date = 2026-08-17T22:00:00+08:00
weight = 52
type = "docs"
description = "解引用 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/50_zh-cn.html](https://tourofrust.com/50_zh-cn.html)

# 解引用

使用 `&mut` 引用时, 你可以通过 `*` 操作符来修改其指向的值。 你也可以使用 `*` 操作符来对所拥有的值进行拷贝（前提是该值可以被拷贝——我们将会在后续章节中讨论可拷贝类型）。

## 示例代码

```rust
fn main() {
    let mut foo = 42;
    let f = &mut foo;
    let bar = *f; // 取得所有者值的拷贝
    *f = 13;      // 设置引用所有者的值
    println!("{}", bar);
    println!("{}", foo);
}
```
