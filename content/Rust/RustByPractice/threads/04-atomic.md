+++
title = "04-线程同步：Atomic"
date = 2026-08-12T20:00:00+08:00
weight = 71
type = "docs"
description = "线程同步：Atomic — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust.beatai.org/threads/atomic.html](https://practice-rust.beatai.org/threads/atomic.html)

# 线程同步：Atomic

`Atomic*` 类型提供无锁原子操作，适合简单的计数器等场景。

1. 🌟
```rust
// 让代码工作
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use std::thread;

fn main() {
    let counter = Arc::new(AtomicUsize::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        handles.push(thread::spawn(move || {
            counter.fetch_add(1, Ordering::SeqCst);
        }));
    }

    for h in handles {
        h.join().unwrap();
    }

    assert_eq!(counter.load(Ordering::SeqCst), 10);
    println!("Success!");
}
```

2. 🌟🌟
```rust
// 填空
use std::sync::atomic::{AtomicBool, Ordering};

fn main() {
    let flag = AtomicBool::new(false);
    flag.store(true, Ordering::Relaxed);
    assert_eq!(flag.load(__), true);
    println!("Success!");
}
```

3. 🌟🌟
```rust
// 让代码工作
use std::sync::atomic::{AtomicI32, Ordering};
use std::sync::Arc;
use std::thread;

fn main() {
    let sum = Arc::new(AtomicI32::new(0));
    let mut handles = vec![];

    for i in 1..=5 {
        let sum = Arc::clone(&sum);
        handles.push(thread::spawn(move || {
            sum.fetch_add(i, Ordering::SeqCst);
        }));
    }

    for h in handles {
        h.join().unwrap();
    }

    assert_eq!(sum.load(Ordering::SeqCst), 15);
    println!("Success!");
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice)找到答案（在 solutions 路径下），但请只在需要时使用
