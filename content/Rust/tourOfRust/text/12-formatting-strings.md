+++
title = "12-字符串格式化"
date = 2026-08-17T22:00:00+08:00
weight = 72
type = "docs"
description = "字符串格式化 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/70_zh-cn.html](https://tourofrust.com/70_zh-cn.html)

# 字符串格式化

宏 `format!` 可用于创建一个使用占位符的参数化字符串。（例：`{}`）

`format!` 和 `println!` 生成的参数化字符串相同，只是 `format!` 将其返回而 `println!` 将其打印出来。

这个函数涉及的内容太过广泛，因而不可能在 *Rust 语言之旅* 中详细介绍，  如需了解完整的内容可看[这里](https://doc.rust-lang.org/std/fmt/)。

## 示例代码

```rust
fn main() {
    let a = 42;
    let f = format!("生活诀窍: {}",a);
    println!("{}",f);
}
```
