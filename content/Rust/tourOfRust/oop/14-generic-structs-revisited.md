+++
title = "14-重温泛型结构体"
date = 2026-08-17T22:00:00+08:00
weight = 89
type = "docs"
description = "重温泛型结构体 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/87_zh-cn.html](https://tourofrust.com/87_zh-cn.html)

# 重温泛型结构体

泛型结构体也可以通过 Trait 来约束其参数化类型：

```rust
struct MyStruct<T>
where
    T: MyTrait
{
    foo: T
    ...
}
```

泛型结构体在它的实现块中有其参数化的类型：

```rust
impl<T> MyStruct<T> {
    ...
}
```
