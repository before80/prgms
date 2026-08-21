+++
title = "02-指针"
date = 2026-08-17T22:00:00+08:00
weight = 93
type = "docs"
description = "指针 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/91_zh-cn.html](https://tourofrust.com/91_zh-cn.html)

# 指针

引用可以转换成一个更原始的类型，指针(raw pointer)。 像数字一样，它可以不受限制地复制和传递，但是Rust 不保证它指向的内存位置的有效性。
有两种指针类型：
* `*const T` - 指向永远不会改变的 T 类型数据的指针。
* `*mut T` - 指向可以更改的 T 类型数据的指针。

指针可以与数字相互转换（例如`usize`）。    
指针可以使用 *unsafe* 代码访问数据（稍后会详细介绍）。

内存细节： 
  * Rust中的引用在用法上与 C 中的指针非常相似，但在如何存储和传递给其他函数上有更多的编译时间限制。
  * Rust中的指针类似于 C 中的指针，它表示一个可以复制或传递的数字，甚至可以转换为数字类型，可以将其修改为数字以进行指针数学运算。

## 示例代码

```rust
fn main() {
    let a = 42;
    let memory_location = &a as *const i32 as usize;
    println!("Data is here {}", memory_location);
}
```
