+++
title = "01-可变变量"
date = 2026-08-20T21:20:00+08:00
weight = 22
type = "docs"
description = "可变变量 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/variable_bindings/mut.html](https://doc.rust-lang.org/stable/rust-by-example/variable_bindings/mut.html)

# 可变变量

变量绑定默认是不可变的（immutable），但加上 `mut` 修饰语后变量就可以改变。

```rust
fn main() {
    let _immutable_binding = 1;
    let mut mutable_binding = 1;

    println!("Before mutation: {}", mutable_binding);

    // 正确代码
    mutable_binding += 1;

    println!("After mutation: {}", mutable_binding);

    // 错误！
    _immutable_binding += 1;
    // 改正 ^ 将此行注释掉
}
```
编译器会给出关于变量可变性的详细诊断信息。
