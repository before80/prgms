+++
title = "06-从循环中返回值"
date = 2026-08-17T22:00:00+08:00
weight = 21
type = "docs"
description = "从循环中返回值 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/19_zh-cn.html](https://tourofrust.com/19_zh-cn.html)

# 从循环中返回值

`loop` 可以被中断以返回一个值。

## 示例代码

```rust
fn main() {
    let mut x = 0;
    let v = loop {
        x += 1;
        if x == 13 {
            break "found the 13";
        }
    };
    println!("from loop: {}", v);
}
```
