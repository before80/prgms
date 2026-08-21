+++
title = "02-变量"
date = 2026-08-17T22:00:00+08:00
weight = 5
type = "docs"
description = "变量 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/03_zh-cn.html](https://tourofrust.com/03_zh-cn.html)

# 变量

变量使用 **let** 关键字来声明。

在赋值时，Rust 能够在 99% 的情况下自动推断其类型。如果不能，你也可以手动将类型添加到变量声明中。

你也许注意到了，我们可以对同一个变量名进行多次赋值。这就是所谓的变量隐藏，可以更改变量类型以实现对该变量名的后续使用。

变量名总是遵循 `蛇形命名法` (snake_case)。

## 示例代码

```rust
fn main() {
    // rust 推断出x的类型
    let x = 13;
    println!("{}", x);

    // rust也可以显式声明类型
    let x: f64 = 3.14159;
    println!("{}", x);

    // rust 也支持先声明后初始化，但很少这样做
    let x;
    x = 0;
    println!("{}", x);
}
```
