+++
title = "03-线程同步：锁、Condvar和信号量"
date = 2026-08-12T20:00:00+08:00
weight = 70
type = "docs"
description = "线程同步：锁、Condvar和信号量 — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust.beatai.org/threads/sync.html](https://practice-rust.beatai.org/threads/sync.html)

# 线程同步：锁、Condvar和信号量

多线程共享可变数据时，常用 `Mutex<T>` 配合 `Arc<T>` 实现安全共享。

1. 🌟
```rust
// 让代码工作
use std::sync::Mutex;

fn main() {
    let m = Mutex::new(5);

    {
        let mut num = m.lock().unwrap();
        *num = 6;
    }

    assert_eq!(*m.lock().unwrap(), 6);
    println!("Success!");
}
```

2. 🌟🌟
```rust
// 让代码工作
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    assert_eq!(*counter.lock().unwrap(), 10);
    println!("Success!");
}
```

3. 🌟🌟
```rust
// 填空
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let data = Arc::new(Mutex::new(vec![]));
    let mut handles = vec![];

    for i in 0..3 {
        let data = Arc::clone(&data);
        handles.push(thread::spawn(move || {
            let mut v = data.lock().unwrap();
            v.push(i);
        }));
    }

    for h in handles {
        h.join().unwrap();
    }

    let v = data.lock().unwrap();
    assert_eq!(v.len(), 3);
    println!("Success!");
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice)找到答案（在 solutions 路径下），但请只在需要时使用
