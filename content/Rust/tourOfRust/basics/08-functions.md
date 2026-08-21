+++
title = "08-函数"
date = 2026-08-17T22:00:00+08:00
weight = 11
type = "docs"
description = "函数 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/09_zh-cn.html](https://tourofrust.com/09_zh-cn.html)

# 函数

函数可以有 0 个或者多个参数。

在这个例子中，add 接受类型为 `i32`（32 位长度的整数）的两个参数。

函数名总是遵循 `蛇形命名法` (snake_case)。

## 示例代码

```rust
fn add(x: i32, y: i32) -> i32 {
    return x + y;
}

fn main() {
    println!("{}", add(42, 13));
}
```
