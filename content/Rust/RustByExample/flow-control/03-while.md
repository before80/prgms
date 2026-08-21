+++
title = "03-while 循环"
date = 2026-08-20T21:20:00+08:00
weight = 41
type = "docs"
description = "while 循环 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/flow_control/while.html](https://doc.rust-lang.org/stable/rust-by-example/flow_control/while.html)

# while 循环

`while` 关键字可以用作当型循环（当条件满足时循环）。

让我们用 `while` 循环写一下臭名昭著的 [FizzBuzz][fizzbuzz]（译者补充：[LeetCode 上的 FizzBuzz 问题描述][fizzbuzz-leetcode]） 程序。

```rust
fn main() {
    // 计数器变量
    let mut n = 1;

    // 当 `n` 小于 101 时循环
    while n < 101 {
        if n % 15 == 0 {
            println!("fizzbuzz");
        } else if n % 3 == 0 {
            println!("fizz");
        } else if n % 5 == 0 {
            println!("buzz");
        } else {
            println!("{}", n);
        }

        // 计数器值加 1
        n += 1;
    }
}
```
[fizzbuzz]: https://en.wikipedia.org/wiki/Fizz_buzz
[fizzbuzz-leetcode]: https://leetcode-cn.com/problems/fizz-buzz/
