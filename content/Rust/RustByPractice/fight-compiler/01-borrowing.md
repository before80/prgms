+++
title = "01-借用"
date = 2026-08-12T20:00:00+08:00
weight = 91
type = "docs"
description = "借用 — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust-zh.beatai.org/fight-compiler/borrowing.html](https://practice-rust-zh.beatai.org/fight-compiler/borrowing.html)

# 借用

1. 🌟🌟
```rust
// 不删除任何代码，修复错误
struct test {
    list: Vec<i32>,
    a: i32
}

impl test {
    pub fn new() -> Self {
        test { list:vec![1,2,3,4,5,6,7], a:0 }
    }

    pub fn run(&mut self) {
        for i in self.list.iter() {
            self.do_something(*i)
        }

    }

    pub fn do_something(&mut self, n: i32) {
        self.a = n;
    }
}

fn main() {}
```
> 参考答案：<https://github.com/sunface/rust-by-practice/blob/master/solutions/fight-compiler/borrowing.md>（solutions 路径），仅在需要时查看。
