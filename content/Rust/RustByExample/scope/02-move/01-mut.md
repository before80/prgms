+++
title = "01-可变性"
date = 2026-08-20T21:20:00+08:00
weight = 104
type = "docs"
description = "可变性 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/scope/move/mut.html](https://doc.rust-lang.org/stable/rust-by-example/scope/move/mut.html)

# 可变性

当所有权转移时，数据的可变性可能发生改变。

```rust
fn main() {
    let immutable_box = Box::new(5u32);

    println!("immutable_box contains {}", immutable_box);

    // 可变性错误
    //*immutable_box = 4;

    // *移动* box，改变所有权（和可变性）
    let mut mutable_box = immutable_box;

    println!("mutable_box contains {}", mutable_box);

    // 修改 box 的内容
    *mutable_box = 4;

    println!("mutable_box now contains {}", mutable_box);
}
```
