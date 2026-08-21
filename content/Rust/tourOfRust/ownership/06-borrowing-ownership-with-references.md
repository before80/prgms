+++
title = "06-使用引用借用所有权"
date = 2026-08-17T22:00:00+08:00
weight = 50
type = "docs"
description = "使用引用借用所有权 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/48_zh-cn.html](https://tourofrust.com/48_zh-cn.html)

# 使用引用借用所有权

引用允许我们通过 `&` 操作符来借用对一个资源的访问权限。
引用也会如同其他资源一样被释放。

## 示例代码

```rust
struct Foo {
    x: i32,
}

fn main() {
    let foo = Foo { x: 42 };
    let f = &foo;
    println!("{}", f.x);
    // f 在这里被 dropped 释放
    // foo 在这里被 dropped 释放
}
```
