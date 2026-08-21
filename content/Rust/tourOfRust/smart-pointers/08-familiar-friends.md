+++
title = "08-熟悉的朋友"
date = 2026-08-17T22:00:00+08:00
weight = 99
type = "docs"
description = "熟悉的朋友 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/97_zh-cn.html](https://tourofrust.com/97_zh-cn.html)

# 熟悉的朋友

想一想一些我们已经见过的智能指针，例如 `Vec<T>` 和 `String`。   

`Vec<T>` 是一个智能指针，它只拥有一些字节的内存区域。  Rust 编译器不知道这些字节中存在着什么。 智能指针解释从它管理的内存区域获取数据意味着什么，跟踪这些字节中的数据结构开始和结束的位置，最后将指针解引用到数据结构中， 成为一个漂亮干净的可以阅读的接口供我们使用（例如`my_vec[3]`）。   

类似地，`String` 跟踪字节的内存区域，并以编程方式将写入其中的内容限制为始终有效的 `utf-8`，并帮助将该内存区域解引用为类型 `&str`。   

这两种数据结构都使用不安全的解引用指针来完成它们的工作。   

内存细节：   
* Rust 有一个相当于 C 的 `malloc`方法，
 [alloc](https://doc.rust-lang.org/std/alloc/fn.alloc.html) 和 [Layout](https://doc.rust-lang.org/std/alloc/struct.Layout.html ) 
 来获取你自己管理的内存区域。

## 示例代码

```rust
use std::alloc::{alloc, Layout};
use std::ops::Deref;

struct Pie {
    secret_recipe: usize,
}

impl Pie {
    fn new() -> Self {
        // let's ask for 4 bytes
        let layout = Layout::from_size_align(4, 1).unwrap();

        unsafe {
            // allocate and save the memory location as a number
            let ptr = alloc(layout) as *mut u8;
            // use pointer math and write a few 
            // u8 values to memory
            ptr.write(86);
            ptr.add(1).write(14);
            ptr.add(2).write(73);
            ptr.add(3).write(64);

            Pie { secret_recipe: ptr as usize }
        }
    }
}
impl Deref for Pie {
    type Target = f32;
    fn deref(&self) -> &f32 {
        // interpret secret_recipe pointer as a f32 raw pointer
        let pointer = self.secret_recipe as *const f32;
        // dereference it into a return value &f32
        unsafe { &*pointer }
    }
}
fn main() {
    let p = Pie::new();
    // "make a pie" by dereferencing our 
    // Pie struct smart pointer
    println!("{:?}", *p);
}
```
