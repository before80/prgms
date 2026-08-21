+++
title = "01-所有权"
date = 2026-08-17T22:00:00+08:00
weight = 45
type = "docs"
description = "所有权 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/43_zh-cn.html](https://tourofrust.com/43_zh-cn.html)

# 所有权

实例化一个类型并且将其**绑定**到变量名上将会创建一些内存资源，而这些内存资源将会在其整个**生命周期**中被 Rust 编译器检验。 被绑定的变量即为该资源的**所有者**。

## 示例代码

```rust
struct Foo {
    x: i32,
}

fn main() {
    // 我们实例化这个结构体并将其绑定到具体的变量上
    // 来创建内存资源
    let foo = Foo { x: 42 };
    // foo 即为该资源的所有者
}
```
