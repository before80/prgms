+++
title = "09-共享引用计数 Arc"
date = 2026-08-20T21:20:00+08:00
weight = 170
type = "docs"
description = "共享引用计数 Arc — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/std/arc.html](https://doc.rust-lang.org/stable/rust-by-example/std/arc.html)

# 共享引用计数 Arc

当线程之间所有权需要共享时，可以使用`Arc`（共享引用计数，Atomic Reference Counted 缩写）可以使用。这个结构通过 `Clone` 实现可以为内存堆中的值的位置创建一个引用指针，同时增加引用计数器。由于它在线程之间共享所有权，因此当指向某个值的最后一个引用指针退出作用域时，该变量将被删除。

```rust
use std::sync::Arc;
use std::thread;

fn main() {
    // 这个变量声明用来指定其值的地方。
    let apple = Arc::new("the same apple");

    for _ in 0..10 {
        // 这里没有数值说明，因为它是一个指向内存堆中引用的指针。
        let apple = Arc::clone(&apple);

        thread::spawn(move || {
            // 由于使用了Arc，线程可以使用分配在 `Arc` 变量指针位置的值来生成。
            println!("{:?}", apple);
        });
    }
}

```
