+++
title = "05-Send 和 Sync"
date = 2026-08-12T20:00:00+08:00
weight = 72
type = "docs"
description = "Send 和 Sync — Rust By Practice"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Rust By Practice / Rust 语言实战](https://github.com/sunface/rust-by-practice)

> 原文链接: [https://practice-rust.beatai.org/threads/send-sync.html](https://practice-rust.beatai.org/threads/send-sync.html)

# Send 和 Sync

`Send` 表示类型可以安全地在线程间转移所有权；`Sync` 表示类型可以安全地在线程间共享引用。

1. 🌟
```rust
// 以下代码能否编译？若不能，说明原因并修复
use std::thread;

fn main() {
    let v = vec![1, 2, 3];
    let handle = thread::spawn(move || {
        println!("{:?}", v);
    });
    handle.join().unwrap();
    println!("Success!");
}
```

2. 🌟🌟
```rust
// 让代码工作：`Rc` 不是 `Send`，应改用 `Arc`
use std::sync::Arc;
use std::thread;

fn main() {
    let data = Arc::new(5);
    let data2 = Arc::clone(&data);

    let handle = thread::spawn(move || {
        println!("{}", data2);
    });

    handle.join().unwrap();
    println!("{}", data);
    println!("Success!");
}
```

3. 🌟🌟
```rust
// 填空：`Mutex` 保护的类型是 `Sync` 的
use std::sync::{Arc, Mutex};
use std::thread;

fn is_send<T: Send>() {}
fn is_sync<T: Sync>() {}

fn main() {
    is_send::<Arc<Mutex<i32>>>();
    is_sync::<Arc<__>>();
    println!("Success!");
}
```

> 你可以在[这里](https://github.com/sunface/rust-by-practice)找到答案（在 solutions 路径下），但请只在需要时使用
