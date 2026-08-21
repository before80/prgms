+++
title = "06-常量"
date = 2026-08-17T22:00:00+08:00
weight = 9
type = "docs"
description = "常量 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/07_zh-cn.html](https://tourofrust.com/07_zh-cn.html)

# 常量

常量允许我们高效地指定一个在代码中会被多次使用的公共值。不同于像变量一样在使用的时候会被复制，常量会在编译期间直接用它们的值来替换变量的文本标识符。

不同于变量，常量必须始终具有显式的类型。

常量名总是遵循 `全大写蛇形命名法（SCREAMING_SNAKE_CASE）`。

## 示例代码

```rust
const PI: f32 = 3.14159;

fn main() {
    println!(
        "To make an apple {} from scratch, you must first create a universe.",
        PI
    );
}
```
