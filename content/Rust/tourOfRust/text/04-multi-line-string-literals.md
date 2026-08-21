+++
title = "04-多行字符串常量"
date = 2026-08-17T22:00:00+08:00
weight = 64
type = "docs"
description = "多行字符串常量 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/62_zh-cn.html](https://tourofrust.com/62_zh-cn.html)

# 多行字符串常量

Rust 中字符串默认支持分行。


使用 `\` 可以使多行字符串不换行。

## 示例代码

```rust
fn main() {
    let haiku: &'static str = "
        我写下，擦掉，
        再写，再擦，
        然后一朵罂粟花开了。
        - 葛饰北斋";
    println!("{}", haiku);
    
    
    println!("你好 \
    世界"); // 注意11行 世 字前面的空格会被忽略
}
```
