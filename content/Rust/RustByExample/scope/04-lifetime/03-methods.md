+++
title = "03-方法"
date = 2026-08-20T21:20:00+08:00
weight = 113
type = "docs"
description = "方法 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/scope/lifetime/methods.html](https://doc.rust-lang.org/stable/rust-by-example/scope/lifetime/methods.html)

# 方法

方法的标注和函数类似：

```rust
struct Owner(i32);

impl Owner {
    // 标注生命周期，就像独立的函数一样。
    fn add_one<'a>(&'a mut self) { self.0 += 1; }
    fn print<'a>(&'a self) {
        println!("`print`: {}", self.0);
    }
}

fn main() {
    let mut owner  = Owner(18);

    owner.add_one();
    owner.print();
}
```
> 译注：方法一般是不需要标明生命周期的，因为 `self` 的生命周期会赋给所有的输出生命周期参数，详见 [TRPL](https://rustwiki.org/zh-CN/book/ch10-03-lifetime-syntax.html#生命周期省略lifetime-elision)。

### 参见： {#参见}

[方法][methods]

[methods]: ../../fn/01-methods/