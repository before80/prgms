+++
title = "02-消息传递"
date = 2026-08-12T20:00:00+08:00
weight = 69
type = "docs"
description = "消息传递 — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust.beatai.org/threads/message-passing.html](https://practice-rust.beatai.org/threads/message-passing.html)

# 消息传递

Rust 鼓励通过消息传递在线程间通信。`std::sync::mpsc` 提供多生产者、单消费者通道。

1. 🌟
```rust
// 让代码工作
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let val = String::from("hi");
        tx.send(val).unwrap();
    });

    let received = rx.recv().unwrap();
    assert_eq!(received, "hi");
    println!("Success!");
}
```

2. 🌟
```rust
// 让代码工作
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let vals = vec![
            String::from("hi"),
            String::from("from"),
            String::from("the"),
            String::from("thread"),
        ];

        for val in vals {
            tx.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });

    for received in rx {
        println!("Got: {}", received);
    }
    println!("Success!");
}
```

3. 🌟🌟
```rust
// 让代码工作：克隆发送端，多个线程发送消息
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    let tx1 = tx.clone();

    thread::spawn(move || {
        tx.send(String::from("hi")).unwrap();
    });

    thread::spawn(move || {
        tx1.send(String::from("from")).unwrap();
    });

    for received in rx {
        println!("Got: {}", received);
    }
    println!("Success!");
}
```

4. 🌟🌟
```rust
// 填空
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        for i in 0..3 {
            tx.send(i).unwrap();
        }
    });

    assert_eq!(rx.recv().unwrap(), 0);
    assert_eq!(rx.recv().unwrap(), 1);
    assert_eq!(__, 2);
    println!("Success!");
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice)找到答案（在 solutions 路径下），但请只在需要时使用
