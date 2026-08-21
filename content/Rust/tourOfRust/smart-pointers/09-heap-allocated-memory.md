+++
title = "09-堆分配内存"
date = 2026-08-17T22:00:00+08:00
weight = 100
type = "docs"
description = "堆分配内存 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/98_zh-cn.html](https://tourofrust.com/98_zh-cn.html)

# 堆分配内存

`Box` 是一个可以让我们将数据从堆栈移动到堆的智能指针。     

解引用可以让我们以人类更容易理解的方式使用堆分配的数据，就好像它是原始类型一样。

## 示例代码

```rust
struct Pie;

impl Pie {
    fn eat(&self) {
        println!("tastes better on the heap!")
    }
}

fn main() {
    let heap_pie = Box::new(Pie);
    heap_pie.eat();
}
```
