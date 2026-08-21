+++
title = "01-if/else if/else"
date = 2026-08-17T22:00:00+08:00
weight = 16
type = "docs"
description = "if/else if/else — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/14_zh-cn.html](https://tourofrust.com/14_zh-cn.html)

# if/else if/else

Rust 中的代码分支不足为奇。

Rust 的条件判断没有括号！~~需要括号干什么。~~我们现有的逻辑就看起来就很干净整洁呀。

不过呢，所有常见的逻辑运算符仍然适用：`==`，`!=`， `<`， `>`， `<=`， `>=`， `!`， `||`， `&&`

## 示例代码

```rust
fn main() {
    let x = 42;
    if x < 42 {
        println!("less than 42");
    } else if x == 42 {
        println!("is 42");
    } else {
        println!("greater than 42");
    }
}
```
