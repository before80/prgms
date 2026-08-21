+++
title = "03-释放是分级进行的"
date = 2026-08-17T22:00:00+08:00
weight = 47
type = "docs"
description = "释放是分级进行的 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/45_zh-cn.html](https://tourofrust.com/45_zh-cn.html)

# 释放是分级进行的

删除一个结构体时，结构体本身会先被释放，紧接着才分别释放相应的子结构体并以此类推。

内存细节：
* Rust 通过自动释放内存来帮助确保减少内存泄漏。
* 每个内存资源仅会被释放一次。

## 示例代码

```rust
struct Bar {
    x: i32,
}

struct Foo {
    bar: Bar,
}

fn main() {
    let foo = Foo { bar: Bar { x: 42 } };
    println!("{}", foo.bar.x);
    // foo 首先被 dropped 释放
    // 紧接着是 foo.bar
}
```
