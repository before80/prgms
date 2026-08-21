+++
title = "09-字符串（String）"
date = 2026-08-17T22:00:00+08:00
weight = 69
type = "docs"
description = "字符串（String） — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/67_zh-cn.html](https://tourofrust.com/67_zh-cn.html)

# 字符串（String）

**字符串`String`** 是一个结构体，其持有以堆（heap）的形式在内存中存储的 utf-8 字节序列。

由于它以堆的形式来存储，字符串可以延长、修改等等。这些都是字符串常量（string literals）无法执行的操作。

常用方法：
* `push_str` 用于在字符串的结尾添加字符串常量（&str）。
* `replace` 用于将一段字符串替换为其它的。
* `to_lowercase`/`to_uppercase` 用于大小写转换。
* `trim` 用于去除字符串前后的空格。

如果字符串`String` 被释放（drop）了，其对应的堆内存片段也将被释放。

字符串`String` 可以使用 `+` 运算符来在其结尾处连接一个 `&str` 并将其自身返回。但这个方法可能并不像你想象中的那么人性化。

## 示例代码

```rust
fn main() {
    let mut helloworld = String::from("你好");
    helloworld.push_str(" 世界");
    helloworld = helloworld + "!";
    println!("{}", helloworld);
}
```
