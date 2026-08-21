+++
title = "03-变量先声明"
date = 2026-08-20T21:20:00+08:00
weight = 24
type = "docs"
description = "变量先声明 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/variable_bindings/declare.html](https://doc.rust-lang.org/stable/rust-by-example/variable_bindings/declare.html)

# 变量先声明

可以先声明（declare）变量绑定，后面才将它们初始化（initialize）。但是这种做法很少用，因为这样可能导致使用未初始化的变量。

```rust
fn main() {
    // 声明一个变量绑定
    let a_binding;

    {
        let x = 2;

        // 初始化一个绑定
        a_binding = x * x;
    }

    println!("a binding: {}", a_binding);

    let another_binding;

    // 报错！使用了未初始化的绑定
    println!("another binding: {}", another_binding);
    // 改正 ^ 注释掉此行

    another_binding = 1;

    println!("another binding: {}", another_binding);
}
```
编译器禁止使用未经初始化的变量，因为这会产生未定义行为（undefined behavior）。
