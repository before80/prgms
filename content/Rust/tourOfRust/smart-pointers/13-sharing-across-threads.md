+++
title = "13-线程间共享"
date = 2026-08-17T22:00:00+08:00
weight = 104
type = "docs"
description = "线程间共享 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/102_zh-cn.html](https://tourofrust.com/102_zh-cn.html)

# 线程间共享

`Mutex` 是一种容器数据结构，通常由智能指针持有，它接收数据并让我们借用对其中数据的可变和不可变引用。  这可以防止借用被滥用，因为操作系统一次只限制一个 CPU 线程访问数据，阻塞其他线程，直到原线程完成其锁定的借用。     

多线程超出了 Rust 之旅的范围，但 `Mutex` 是协调多个 CPU 线程访问相同数据的基本部分。    

有一个特殊的智能指针 `Arc`，它与 `Rc` 相同，除了使用线程安全的引用计数递增。 它通常用于对同一个 `Mutex` 进行多次引用。

## 示例代码

```rust
use std::sync::Mutex;

struct Pie;

impl Pie {
    fn eat(&self) {
        println!("only I eat the pie right now!");
    }
}

fn main() {
    let mutex_pie = Mutex::new(Pie);
    // let's borrow a locked immutable reference of pie
    // we have to unwrap the result of a lock
    // because it might fail
    let ref_pie = mutex_pie.lock().unwrap();
    ref_pie.eat();
    // locked reference drops here, and mutex protected value can be used by someone else
}
```
