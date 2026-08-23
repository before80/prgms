+++
title = "01-多线程基础"
date = 2026-08-12T20:00:00+08:00
weight = 68
type = "docs"
description = "多线程基础 — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust.beatai.org/threads/basic-using.html](https://practice-rust.beatai.org/threads/basic-using.html)

# 多线程基础

使用 `std::thread::spawn` 创建新线程，用 `JoinHandle` 的 `join` 等待线程结束。

1. 🌟
```rust
// 让代码工作
use std::thread;
use std::time::Duration;

fn main() {
    thread::spawn(|| {
        for i in 1..3 {
            println!("hi number {} from the spawned thread", i);
            thread::sleep(Duration::from_millis(1));
        }
    });

    for i in 1..3 {
        println!("hi number {} from the main thread", i);
        thread::sleep(Duration::from_millis(1));
    }
    println!("Success!");
}
```

2. 🌟
```rust
// 让代码工作：主线程应等待子线程结束
use std::thread;
use std::time::Duration;

fn main() {
    let handle = thread::spawn(|| {
        for i in 1..3 {
            println!("spawned: {}", i);
            thread::sleep(Duration::from_millis(1));
        }
    });

  __;

    println!("Success!");
}
```

3. 🌟🌟
```rust
// 让代码工作
use std::thread;

fn main() {
    let v = vec![1, 2, 3];

    let handle = thread::spawn(move || {
        println!("Here's a vector: {:?}", v);
    });

    handle.join().unwrap();
    println!("Success!");
}
```

4. 🌟🌟
```rust
// 填空
use std::thread;

fn main() {
    let s = String::from("hello");

    let handle = thread::spawn(move || {
        println!("{}", s);
    });

    // 取消下面这行的注释并修复错误
    // println!("{}", s);

    handle.join().unwrap();
    println!("Success!");
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice)找到答案（在 solutions 路径下），但请只在需要时使用
