+++
title = "01-嵌套循环和标签"
date = 2026-08-20T21:20:00+08:00
weight = 39
type = "docs"
description = "嵌套循环和标签 — Rust By Example"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust By Example](https://doc.rust-lang.org/stable/rust-by-example/)

> 原文链接: [https://doc.rust-lang.org/stable/rust-by-example/flow_control/loop/nested.html](https://doc.rust-lang.org/stable/rust-by-example/flow_control/loop/nested.html)

# 嵌套循环和标签

在处理嵌套循环的时候可以 `break` 或 `continue` 外层循环。在这类情形中，循环必须用一些 `'label`（标签）来注明，并且标签必须传递给 `break`/`continue` 语句。

```rust
#![allow(unreachable_code)]

fn main() {
    'outer: loop {
        println!("Entered the outer loop");

        'inner: loop {
            println!("Entered the inner loop");

            // 这只是中断内部的循环
            //break;

            // 这会中断外层循环
            break 'outer;
        }

        println!("This point will never be reached");
    }

    println!("Exited the outer loop");
}
```
