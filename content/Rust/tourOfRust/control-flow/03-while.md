+++
title = "03-while"
date = 2026-08-17T22:00:00+08:00
weight = 18
type = "docs"
description = "while — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/16_zh-cn.html](https://tourofrust.com/16_zh-cn.html)

# while

`while` 允许你轻松地向循环添加条件。

如果条件一旦变为 `false`，循环就会退出。

## 示例代码

```rust
fn main() {
    let mut x = 0;
    while x != 42 {
        x += 1;
    }
}
```
