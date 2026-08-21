+++
title = "10-将文本作为函数的参数"
date = 2026-08-17T22:00:00+08:00
weight = 70
type = "docs"
description = "将文本作为函数的参数 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/68_zh-cn.html](https://tourofrust.com/68_zh-cn.html)

# 将文本作为函数的参数

字符串常量（String literals）和字符串（String）一般以字符串片段（string slice）的形式传递给函数。这给许多场景提供了充足的灵活性，因为所有权并未被传递。

## 示例代码

```rust
fn say_it_loud(msg:&str){
    println!("{}！！！",msg.to_string().to_uppercase());
}

fn main() {
    // say_it_loud can borrow &'static str as a &str
    say_it_loud("你好");
    // say_it_loud can also borrow String as a &str
    say_it_loud(&String::from("再见"));
}
```
