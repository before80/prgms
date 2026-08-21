+++
title = "05-基本类型转换"
date = 2026-08-17T22:00:00+08:00
weight = 8
type = "docs"
description = "基本类型转换 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/06_zh-cn.html](https://tourofrust.com/06_zh-cn.html)

# 基本类型转换

当涉及到数字类型时，Rust 要求明确。一个人不能想当然地把“u8”用在“u32”上而不出错。

幸运的是，使用 **as** 关键字，Rust 使数字类型转换非常容易。

## 示例代码

```rust
fn main() {
    let a = 13u8;
    let b = 7u32;
    let c = a as u32 + b;
    println!("{}", c);

    let t = true;
    println!("{}", t as u8);
}
```
