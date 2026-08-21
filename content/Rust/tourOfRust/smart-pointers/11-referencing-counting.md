+++
title = "11-引用计数"
date = 2026-08-17T22:00:00+08:00
weight = 102
type = "docs"
description = "引用计数 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/100_zh-cn.html](https://tourofrust.com/100_zh-cn.html)

# 引用计数

`Rc` 是一个能将数据从栈移动到智能指针。       它允许我们克隆其他`Rc`智能指针，这些指针都具有不可改变地借用放在堆上的数据的能力。    

只有当最后一个智能指针被删除时，堆上的数据才会被释放。

## 示例代码

```rust
use std::rc::Rc;

struct Pie;

impl Pie {
    fn eat(&self) {
        println!("tastes better on the heap!")
    }
}

fn main() {
    let heap_pie = Rc::new(Pie);
    let heap_pie2 = heap_pie.clone();
    let heap_pie3 = heap_pie2.clone();

    heap_pie3.eat();
    heap_pie2.eat();
    heap_pie.eat();

    // all reference count smart pointers are dropped now
    // the heap data Pie finally deallocates
}
```
