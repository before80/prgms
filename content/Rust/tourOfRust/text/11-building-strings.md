+++
title = "11-字符串构建"
date = 2026-08-17T22:00:00+08:00
weight = 71
type = "docs"
description = "字符串构建 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/69_zh-cn.html](https://tourofrust.com/69_zh-cn.html)

# 字符串构建

`concat` 和 `join` 可以以简洁而有效的方式构建字符串。

## 示例代码

```rust
fn main() {
    let helloworld = ["你好", " ", "世界", "！"].concat();
    let abc = ["a", "b", "c"].join(",");
    println!("{}", helloworld);
    println!("{}",abc);
}
```
