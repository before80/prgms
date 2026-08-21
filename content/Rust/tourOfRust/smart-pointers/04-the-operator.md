+++
title = "04-运算符 *"
date = 2026-08-17T22:00:00+08:00
weight = 95
type = "docs"
description = "运算符 * — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/93_zh-cn.html](https://tourofrust.com/93_zh-cn.html)

# 运算符 *

`*` 运算符是一种很明确的解引用的方法。
```rust
let a: i32 = 42;
let ref_ref_ref_a: &&&i32 = &&&a;
let ref_a: &i32 = **ref_ref_ref_a;
let b: i32 = *ref_a;
```
内存细节:
  - 因为 i32 是实现了 `Copy` 特性的原始类型，堆栈上变量 `a` 的字节被复制到变量 `b` 的字节中。

## 示例代码

```rust
fn main() {
    let a: i32 = 42;
    let ref_ref_ref_a: &&&i32 = &&&a;
    let ref_a: &i32 = **ref_ref_ref_a;
    let b: i32 = *ref_a;
    println!("{}", b)
}
```
