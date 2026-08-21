+++
title = "05-类元组结构体"
date = 2026-08-17T22:00:00+08:00
weight = 29
type = "docs"
description = "类元组结构体 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/27_zh-cn.html](https://tourofrust.com/27_zh-cn.html)

# 类元组结构体

简洁起见，你可以创建像元组一样被使用的结构体。

## 示例代码

```rust
struct Location(i32, i32);

fn main() {
    // 这仍然是一个在栈上的结构体
    let loc = Location(42, 32);
    println!("{}, {}", loc.0, loc.1);
}
```
