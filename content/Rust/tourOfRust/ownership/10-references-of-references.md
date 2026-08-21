+++
title = "10-引用的引用"
date = 2026-08-17T22:00:00+08:00
weight = 54
type = "docs"
description = "引用的引用 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/52_zh-cn.html](https://tourofrust.com/52_zh-cn.html)

# 引用的引用

引用甚至也可以用在其他引用上。

## 示例代码

```rust
#[derive(Debug)]
struct Foo {
    x: i32,
}
fn do_something(a: &Foo) -> &i32 {
    return &a.x;
}

fn main() {
    let mut foo = Foo { x: 42 };
    let x = &mut foo.x;
    *x = 13;
    // x 在这里被 dropped 释放从而允许我们再创建一个不可变引用
    let y = do_something(&foo);
    println!("{}", y);//13
    // y 在这里被 dropped 释放
    // foo 在这里被 dropped 释放
}
```
