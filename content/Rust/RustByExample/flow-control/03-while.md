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

​	`while` 关键字可以用作当型循环（当条件满足时循环）。

​	让我们用 `while` 循环写一下臭名昭著的 [FizzBuzz][fizzbuzz]（译者补充：[LeetCode 上的 FizzBuzz 问题描述][fizzbuzz-leetcode]） 程序。

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
//
1
2
fizz
4
buzz
fizz
7
8
fizz
buzz
11
fizz
13
14
fizzbuzz
16
17
fizz
19
buzz
fizz
22
23
fizz
buzz
26
fizz
28
29
fizzbuzz
31
32
fizz
34
buzz
fizz
37
38
fizz
buzz
41
fizz
43
44
fizzbuzz
46
47
fizz
49
buzz
fizz
52
53
fizz
buzz
56
fizz
58
59
fizzbuzz
61
62
fizz
64
buzz
fizz
67
68
fizz
buzz
71
fizz
73
74
fizzbuzz
76
77
fizz
79
buzz
fizz
82
83
fizz
buzz
86
fizz
88
89
fizzbuzz
91
92
fizz
94
buzz
fizz
97
98
fizz
buzz
```
[fizzbuzz]: https://en.wikipedia.org/wiki/Fizz_buzz
[fizzbuzz-leetcode]: https://leetcode-cn.com/problems/fizz-buzz/
