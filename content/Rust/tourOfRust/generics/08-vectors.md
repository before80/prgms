+++
title = "08-Vectors"
date = 2026-08-17T22:00:00+08:00
weight = 42
type = "docs"
description = "Vectors — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/40_zh-cn.html](https://tourofrust.com/40_zh-cn.html)

# Vectors

一些经常使用的泛型是集合类型。一个 vector 是可变长度的元素集合，以 `Vec` 结构表示。

比起手动构建，宏 `vec!` 让我们可以轻松地创建 vector。

`Vec` 有一个形如 `iter()` 的方法可以为一个 vector 创建迭代器，这允许我们可以轻松地将 vector 用到 `for` 循环中去。

内存细节：
* `Vec` 是一个结构体，但是内部其实保存了在堆上固定长度数据的引用。
* 一个 vector 开始有默认大小容量，当更多的元素被添加进来后，它会重新在堆上分配一个新的并具有更大容量的定长列表。（类似 C++ 的 vector）

## 示例代码

```rust
fn main() {
    // 我们可以显式确定类型
    let mut i32_vec = Vec::<i32>::new(); // turbofish <3
    i32_vec.push(1);
    i32_vec.push(2);
    i32_vec.push(3);

    // 但是看看 Rust 是多么聪明的自动检测类型啊
    let mut float_vec = Vec::new();
    float_vec.push(1.3);
    float_vec.push(2.3);
    float_vec.push(3.4);

    // 这是个漂亮的宏！
    let string_vec = vec![String::from("Hello"), String::from("World")];

    for word in string_vec.iter() {
        println!("{}", word);
    }
}
```
