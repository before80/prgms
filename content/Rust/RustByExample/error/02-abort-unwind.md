+++
title = "02-`abort` 与 `unwind`"
date = 2026-08-20T21:20:00+08:00
weight = 140
type = "docs"
description = "`abort` 与 `unwind` — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/error/abort_unwind.html](https://doc.rust-lang.org/stable/rust-by-example/error/abort_unwind.html)

# `abort` 与 `unwind`

上一节介绍了错误处理机制 `panic`。可以根据 panic 设置有条件地编译不同代码路径。当前可用的值是 `unwind` 与 `abort`。

在先前柠檬水示例的基础上，我们显式使用 panic 策略来执行不同代码行。

```rust
fn drink(beverage: &str) {
    // 你不该喝太多含糖饮料。
    if beverage == "lemonade" {
        if cfg!(panic = "abort") {
            println!("This is not your party. Run!!!!");
        } else {
            println!("Spit it out!!!!");
        }
    } else {
        println!("Some refreshing {} is all I need.", beverage);
    }
}

fn main() {
    drink("water");
    drink("lemonade");
}
```
下面再看一个例子：改写 `drink()`，并显式使用 `unwind` 关键字。

```rust
#[cfg(panic = "unwind")]
fn ah() {
    println!("Spit it out!!!!");
}

#[cfg(not(panic = "unwind"))]
fn ah() {
    println!("This is not your party. Run!!!!");
}

fn drink(beverage: &str) {
    if beverage == "lemonade" {
        ah();
    } else {
        println!("Some refreshing {} is all I need.", beverage);
    }
}

fn main() {
    drink("water");
    drink("lemonade");
}
```
可通过命令行使用 `abort` 或 `unwind` 设置 panic 策略。

```console
rustc  lemonade.rs -C panic=abort
```
