+++
title = "07-程序参数"
date = 2026-08-20T21:20:00+08:00
weight = 184
type = "docs"
description = "程序参数 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/std_misc/arg.html](https://doc.rust-lang.org/stable/rust-by-example/std_misc/arg.html)

# 程序参数

## 标准库 {#标准库}

命令行参数可使用 `std::env::args` 进行接收，这将返回一个迭代器，该迭代器会对每个参数举出一个字符串。

```rust
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();

    // 第一个参数是调用本程序的路径
    println!("My path is {}.", args[0]);

    // 其余的参数是被传递给程序的命令行参数。
    // 请这样调用程序：
    //   $ ./args arg1 arg2
    println!("I got {:?} arguments: {:?}.", args.len() - 1, &args[1..]);
}
```
```bash
$ ./args 1 2 3
My path is ./args.
I got 3 arguments: ["1", "2", "3"].
```
## crate {#crate}

另外，也有很多 crate 提供了编写命令行应用的额外功能。[Rust Cookbook] 展示了使用最流行的命令行参数 crate，即 `clap` 的最佳实践。

[Rust Cookbook]: https://rust-lang-nursery.github.io/rust-cookbook/app.html#ex-clap-basic
