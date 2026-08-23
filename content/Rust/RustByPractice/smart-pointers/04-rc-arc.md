+++
title = "04-Rc and Arc"
date = 2026-08-12T20:00:00+08:00
weight = 63
type = "docs"
description = "Rc and Arc — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust.beatai.org/smart-pointers/rc-arc.html](https://practice-rust.beatai.org/smart-pointers/rc-arc.html)

# Rc and Arc

`Rc<T>` 用于单线程下的引用计数；`Arc<T>` 是线程安全的原子引用计数，常用于多线程共享数据。

1. 🌟
```rust
// 让代码工作
use std::rc::Rc;

fn main() {
    let a = Rc::new(5);
    let b = Rc::clone(&a);
    assert_eq!(Rc::strong_count(&a), 2);
    assert_eq!(*a + *b, 10);
    println!("Success!");
}
```

2. 🌟
```rust
// 让代码工作
use std::rc::Rc;

#[derive(Debug)]
enum List {
    Cons(i32, Rc<List>),
    Nil,
}

use List::{Cons, Nil};

fn main() {
    let a = Rc::new(Cons(5, Rc::new(Cons(10, Rc::new(Nil)))));
    let b = Cons(3, Rc::clone(&a));
    println!("a count = {}", Rc::strong_count(&a));
    println!("Success!");
}
```

3. 🌟🌟
```rust
// 让代码工作
use std::sync::Arc;
use std::thread;

fn main() {
    let counter = Arc::new(0);
    let mut handles = vec![];

    for _ in 0..3 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            // 此处不能直接修改 Arc 内的值
            let _ = counter;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }
    assert_eq!(*counter, 0);
    println!("Success!");
}
```

4. 🌟🌟
```rust
// 填空：使用 Arc 在线程间共享向量长度
use std::sync::Arc;
use std::thread;

fn main() {
    let v = vec![1, 2, 3];
    let shared = Arc::new(v);
    let len = shared.len();

    let handle = thread::spawn(move || {
        len
    });

    assert_eq!(handle.join().unwrap(), 3);
    println!("Success!");
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice)找到答案（在 solutions 路径下），但请只在需要时使用
