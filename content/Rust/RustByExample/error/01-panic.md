+++
title = "01-`panic`"
date = 2026-08-20T21:20:00+08:00
weight = 139
type = "docs"
description = "`panic` — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/error/panic.html](https://doc.rust-lang.org/stable/rust-by-example/error/panic.html)

# `panic`

我们将要看到的最简单的错误处理机制就是 `panic`。它会打印一个错误消息，开始回退（unwind）任务，且通常会退出程序。这里我们显式地在错误条件下调用 `panic`：

```rust
fn give_princess(gift: &str) {
    // 公主讨厌蛇，所以如果公主表示厌恶的话我们要停止！
    if gift == "snake" { panic!("AAAaaaaa!!!!"); }

    println!("I love {}s!!!!!", gift);
}

fn main() {
    give_princess("teddy bear");
    give_princess("snake");
}
```
