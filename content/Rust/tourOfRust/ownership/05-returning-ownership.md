+++
title = "05-归还所有权"
date = 2026-08-17T22:00:00+08:00
weight = 49
type = "docs"
description = "归还所有权 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/47_zh-cn.html](https://tourofrust.com/47_zh-cn.html)

# 归还所有权

所有权也可以从一个函数中被归还。

## 示例代码

```rust
struct Foo {
    x: i32,
}

fn do_something() -> Foo {
    Foo { x: 42 }
    // 所有权被移出
}

fn main() {
    let foo = do_something();
    // foo 成为了所有者
    // foo 在函数域结尾被 dropped 释放
}
```
