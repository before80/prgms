+++
title = "12-共享访问"
date = 2026-08-17T22:00:00+08:00
weight = 103
type = "docs"
description = "共享访问 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/101_zh-cn.html](https://tourofrust.com/101_zh-cn.html)

# 共享访问

`RefCell` 是一个容器数据结构，通常由智能指针拥有，它接收数据并让我们借用可变或不可变引用来访问内部内容。 当您要求借用数据时，它通过在运行时强制执行 Rust 的内存安全规则来防止借用被滥用     

**只有一个可变引用或多个不可变引用，但不能同时有！**  

如果你违反了这些规则，`RefCell` 将会panic。

## 示例代码

```rust
use std::cell::RefCell;

struct Pie {
    slices: u8
}

impl Pie {
    fn eat(&mut self) {
        println!("tastes better on the heap!");
        self.slices -= 1;
    }
}

fn main() {
    // RefCell validates memory safety at runtime
    // notice: pie_cell is not mut!
    let pie_cell = RefCell::new(Pie{slices:8});
    
    {
        // but we can borrow mutable references!
        let mut mut_ref_pie = pie_cell.borrow_mut();
        mut_ref_pie.eat();
        mut_ref_pie.eat();
        
        // mut_ref_pie is dropped at end of scope
    }
    
    // now we can borrow immutably once our mutable reference drops
     let ref_pie = pie_cell.borrow();
     println!("{} slices left",ref_pie.slices);
}
```
