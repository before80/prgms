+++
title = "05-原始字符串常量"
date = 2026-08-17T22:00:00+08:00
weight = 65
type = "docs"
description = "原始字符串常量 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/63_zh-cn.html](https://tourofrust.com/63_zh-cn.html)

# 原始字符串常量

原始字符串支持写入原始的文本而无需为特殊字符转义，因而不会导致可读性下降（如双引号与反斜杠无需写为 `\"` 和 `\\`），只需以 `r#"` 开头，以 `"#` 结尾。

## 示例代码

```rust
fn main() {
    let a: &'static str = r#"
        <div class="advice">
            原始字符串在一些情景下非常有用。
        </div>
        "#;
    println!("{}", a);
}
```
