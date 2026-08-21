+++
title = "04-for"
date = 2026-08-17T22:00:00+08:00
weight = 19
type = "docs"
description = "for — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/17_zh-cn.html](https://tourofrust.com/17_zh-cn.html)

# for

Rust 的 `for` 循环是一个强大的升级。它遍历来自计算结果为迭代器的任意表达式的值。
迭代器是什么？迭代器是一个你可以一直询问“下一项是什么？”直到没有其他项的对象。

我们将在以后的章节中进一步探讨这一点，与此同时，我们知道 Rust 使创建生成整数序列的迭代器变得容易。

`..` 运算符创建一个可以生成包含起始数字、但不包含末尾数字的数字序列的迭代器。

`..=` 运算符创建一个可以生成包含起始数字、且包含末尾数字的数字序列的迭代器。

## 示例代码

```rust
fn main() {
    for x in 0..5 {
        println!("{}", x);
    }

    for x in 0..=5 {
        println!("{}", x);
    }
}
```
