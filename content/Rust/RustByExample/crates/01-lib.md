+++
title = "01-库"
date = 2026-08-20T21:20:00+08:00
weight = 75
type = "docs"
description = "库 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/crates/lib.html](https://doc.rust-lang.org/stable/rust-by-example/crates/lib.html)

# 库

让我们创建一个库，然后看看如何把它链接到另一个 crate。

```rust
pub fn public_function() {
    println!("called rary's `public_function()`");
}

fn private_function() {
    println!("called rary's `private_function()`");
}

pub fn indirect_access() {
    print!("called rary's `indirect_access()`, that\n> ");

    private_function();
}
```
```bash
$ rustc --crate-type=lib rary.rs
$ ls lib*
library.rlib
```
默认情况下，库会使用 crate 文件的名字，前面加上 “lib” 前缀，但这个默认名称可以使用 [`crate_name` 属性][crate-name] 覆盖。

[crate-name]: ../attribute/02-crate/