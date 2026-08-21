+++
title = "04-移交所有权"
date = 2026-08-17T22:00:00+08:00
weight = 48
type = "docs"
description = "移交所有权 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/46_zh-cn.html](https://tourofrust.com/46_zh-cn.html)

# 移交所有权

将所有者作为参数传递给函数时，其所有权将移交至该函数的参数。 在一次**移动**后，原函数中的变量将无法再被使用。

内存细节:
* 在**移动**期间，所有者的堆栈值将会被复制到函数调用的参数堆栈中。

## 示例代码

```rust
struct Foo {
    x: i32,
}

fn do_something(f: Foo) {
    println!("{}", f.x);
    // f 在这里被 dropped 释放
}

fn main() {
    let foo = Foo { x: 42 };
    // foo 被移交至 do_something
    do_something(foo);
    // 此后 foo 便无法再被使用
}
```
