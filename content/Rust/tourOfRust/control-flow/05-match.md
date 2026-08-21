+++
title = "05-match"
date = 2026-08-17T22:00:00+08:00
weight = 20
type = "docs"
description = "match — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/18_zh-cn.html](https://tourofrust.com/18_zh-cn.html)

# match

想念你的 switch 语句吗？Rust 有一个非常有用的关键字，用于匹配值的所有可能条件，
并在匹配为真时执行相应代码。我们先来看看对数字的使用。在未来章节中，我们将有更多
更复杂的数据模式匹配的说明，我向你保证，它将值得等待。

`match` 是穷尽的，意为所有可能的值都必须被考虑到。

匹配与解构相结合是迄今为止你在 Rust 中看到的最常见的模式之一。

## 示例代码

```rust
fn main() {
    let x = 42;

    match x {
        0 => {
            println!("found zero");
        }
        // 我们可以匹配多个值
        1 | 2 => {
            println!("found 1 or 2!");
        }
        // 我们可以匹配迭代器
        3..=9 => {
            println!("found a number 3 to 9 inclusively");
        }
        // 我们可以将匹配数值绑定到变量
        matched_num @ 10..=100 => {
            println!("found {} number between 10 to 100!", matched_num);
        }
        // 这是默认匹配，如果没有处理所有情况，则必须存在该匹配
        _ => {
            println!("found something else!");
        }
    }
}
```
