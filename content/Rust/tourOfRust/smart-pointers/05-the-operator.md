+++
title = "05-运算符 ."
date = 2026-08-17T22:00:00+08:00
weight = 96
type = "docs"
description = "运算符 . — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/94_zh-cn.html](https://tourofrust.com/94_zh-cn.html)

# 运算符 .

`.`运算符用于访问引用的字段和方法，它的工作原理更加巧妙。

```rust
let f = Foo { value: 42 };
let ref_ref_ref_f = &&&f;
println!("{}", ref_ref_ref_f.value);
```
哇，为什么我们不需要在`ref_ref_ref_f`之前添加`***`？这是因为 `.` 运算符会做一些列自动解引用操作。 最后一行由编译器自动转换为以下内容。
```rust
println!("{}", (***ref_ref_ref_f).value);
```

## 示例代码

```rust
struct Foo {
    value: i32
}

fn main() {
    let f = Foo { value: 42 };
    let ref_ref_ref_f = &&&f;
    println!("{}", ref_ref_ref_f.value);
}
```
