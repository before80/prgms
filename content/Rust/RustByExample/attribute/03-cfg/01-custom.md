+++
title = "01-自定义条件"
date = 2026-08-20T21:20:00+08:00
weight = 86
type = "docs"
description = "自定义条件 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/attribute/cfg/custom.html](https://doc.rust-lang.org/stable/rust-by-example/attribute/cfg/custom.html)

# 自定义条件

有部分条件如 `target_os` 是由 `rustc` 隐式地提供的，但是自定义条件必须使用
 `--cfg` 标记来传给 `rustc`。

```rust
#[cfg(some_condition)]
fn conditional_function() {
    println!("condition met!")
}

fn main() {
    conditional_function();
}
```
试试不使用自定义的 `cfg` 标记会发生什么：

```bash
$ rustc custom.rs && ./custom
No such file or directory (os error 2)
```
使用自定义的 `cfg` 标记：

```bash
$ rustc --cfg some_condition custom.rs && ./custom
condition met!
```
