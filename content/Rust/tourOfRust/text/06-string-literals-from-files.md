+++
title = "06-文件中的字符串常量"
date = 2026-08-17T22:00:00+08:00
weight = 66
type = "docs"
description = "文件中的字符串常量 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/64_zh-cn.html](https://tourofrust.com/64_zh-cn.html)

# 文件中的字符串常量

如果你需要使用大量文本，可以尝试用宏 `include_str!` 来从本地文件中导入文本到程序中：

```rust
let hello_html = include_str!("hello.html");
```
