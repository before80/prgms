+++
title = "10-返回空值"
date = 2026-08-17T22:00:00+08:00
weight = 13
type = "docs"
description = "返回空值 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/11_zh-cn.html](https://tourofrust.com/11_zh-cn.html)

# 返回空值

如果没有为函数指定返回类型，它将返回一个空的元组，也称为*单元*。

一个空的元组用 `()` 表示。

直接使用 `()` 的情况相当不常见。但它经常会出现（比如作为函数返回值），所以了解其来龙去脉非常重要。

## 示例代码

```rust
fn make_nothing() -> () {
    return ();
}

// 返回类型隐含为 ()
fn make_nothing2() {
    // 如果没有指定返回值，这个函数将会返回 ()
}

fn main() {
    let a = make_nothing();
    let b = make_nothing2();

    // 打印a和b的debug字符串，因为很难去打印空
    println!("The value of a: {:?}", a);
    println!("The value of b: {:?}", b);
}
```
