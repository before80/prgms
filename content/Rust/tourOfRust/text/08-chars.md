+++
title = "08-Char"
date = 2026-08-17T22:00:00+08:00
weight = 68
type = "docs"
description = "Char — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/66_zh-cn.html](https://tourofrust.com/66_zh-cn.html)

# Char

为了解决使用 Unicode 带来的麻烦，Rust 提供了将 utf-8 字节序列转化为类型 `char` 的 vector 的方法。

每个 `char` 长度都为 4 字节（可提高字符查找的效率）。

## 示例代码

```rust
fn main() {
    // 收集字符并转换为类型为 char 的 vector
    let chars = "你好 🦀".chars().collect::<Vec<char>>();
    println!("{}", chars.len()); // 结果应为 4
    // 由于 char 为 4 字节长，我们可以将其转化为 u32
    println!("{}", chars[3] as u32);
}
```
