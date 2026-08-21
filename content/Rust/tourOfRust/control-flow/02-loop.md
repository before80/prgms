+++
title = "02-循环"
date = 2026-08-17T22:00:00+08:00
weight = 17
type = "docs"
description = "循环 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/15_zh-cn.html](https://tourofrust.com/15_zh-cn.html)

# 循环

需要一个无限循环？

使用 Rust 很容易实现。

`break` 会退出当前循环。但 `loop` 还有个秘密，我们很快讲到。

## 示例代码

```rust
fn main() {
    let mut x = 0;
    loop {
        x += 1;
        if x == 42 {
            break;
        }
    }
    println!("{}", x);
}
```
