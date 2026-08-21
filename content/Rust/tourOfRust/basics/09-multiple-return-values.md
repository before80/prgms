+++
title = "09-多个返回值"
date = 2026-08-17T22:00:00+08:00
weight = 12
type = "docs"
description = "多个返回值 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/10_zh-cn.html](https://tourofrust.com/10_zh-cn.html)

# 多个返回值

函数可以通过**元组**来返回多个值。

元组元素可以通过他们的索引来获取。

Rust 允许我们将后续会看到的各种形式的解构，也允许我们以符合逻辑的方式提取数据结构的子片段。敬请期待后面的内容！

## 示例代码

```rust
fn swap(x: i32, y: i32) -> (i32, i32) {
    return (y, x);
}

fn main() {
    // 返回一个元组
    let result = swap(123, 321);
    println!("{} {}", result.0, result.1);

    // 将元组解构为两个变量
    let (a, b) = swap(result.0, result.1);
    println!("{} {}", a, b);
}
```
