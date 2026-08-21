+++
title = "07-字符串片段（String Slice）"
date = 2026-08-17T22:00:00+08:00
weight = 67
type = "docs"
description = "字符串片段（String Slice） — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/65_zh-cn.html](https://tourofrust.com/65_zh-cn.html)

# 字符串片段（String Slice）

字符串片段是对内存中字节序列的引用，而且这段字节序列必须是合法的 utf-8 字节序列。

`str` 片段的字符串片段（子片段），也必须是合法的 utf-8 字节序列。

`&str` 的常用方法：
* `len` 获取字符串常量的字节长度（不是字符长度）。
*  `starts_with`/`ends_with` 用于基础测试。
* `is_empty` 长度为 0 时返回 true。
* `find` 返回 `Option<usize>`，其中的 `usize` 为匹配到的第一个对应文本的索引值。

## 示例代码

```rust
fn main() {
    let a = "你好 🦀";
    println!("{}", a.len());
    let first_word = &a[0..6];
    let second_word = &a[7..11];
    // let half_crab = &a[7..9]; 报错
    // Rust 不接受无效 unicode 字符构成的片段
    println!("{} {}", first_word, second_word);
}
```
