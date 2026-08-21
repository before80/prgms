+++
title = "40-&str 的类型"
date = 2026-08-21T12:46:00+08:00
weight = 41
type = "docs"
description = "&str 的类型 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_39.html](https://dhghomon.github.io/easy_rust/Chapter_39.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# &str 的类型

`&str`的类型不止一种。我们有。

- 字符串： 当你写`let my_str = "I am a &str"`的时候，你就会产生这些字符。它们在整个程序中持续存在，因为它们是直接写进二进制中的，它们的类型是 `&'static str`。`'`的意思是它的生命期，字符串字元有一个叫`static`的生命期。
- 借用str：这是常规的 `&str` 形式，没有 `static` 生命期。如果你创建了一个`String`，并得到了它的引用，当你需要它时，Rust会把它转换为`&str`。比如说

```rust
fn prints_str(my_str: &str) { // 可以把 &String 当作 &str 用
    println!("{}", my_str);
}

fn main() {
    let my_string = String::from("I am a string");
    prints_str(&my_string); // 传给 prints_str 一个 &String
}
```

那么什么是lifetime呢？我们现在就来了解一下。
