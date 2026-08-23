+++
title = "02-Deref"
date = 2026-08-12T20:00:00+08:00
weight = 61
type = "docs"
description = "Deref — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust.beatai.org/smart-pointers/deref.html](https://practice-rust.beatai.org/smart-pointers/deref.html)

# Deref

`Deref` trait 允许我们将智能指针当作常规引用对待。通过实现 `Deref`，可以让 `*` 运算符按预期工作。

1. 🌟
```rust
// 让代码工作
use std::ops::Deref;

struct MyBox<T>(T);

impl<T> Deref for MyBox<T> {
    type Target = T;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

fn main() {
    let x = MyBox(5);
    assert_eq!(*x, 5);
    println!("Success!");
}
```

2. 🌟
```rust
// 让代码工作
use std::ops::Deref;

struct MyBox<T>(T);

impl<T> Deref for MyBox<T> {
    type Target = T;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

fn hello(name: &str) {
    println!("Hello, {}!", name);
}

fn main() {
    let m = MyBox(String::from("Rust"));
    hello(&m);
    println!("Success!");
}
```

3. 🌟🌟
```rust
// 填空
use std::ops::{Deref, DerefMut};

struct MyBox<T>(T);

impl<T> Deref for MyBox<T> {
    type Target = T;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl<T> DerefMut for MyBox<T> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

fn main() {
    let mut s = MyBox(String::from("hello"));
    s.__.push_str(", world");
    assert_eq!(*s, "hello, world");
    println!("Success!");
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice)找到答案（在 solutions 路径下），但请只在需要时使用
