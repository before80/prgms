+++
title = "07-智能不安全代码"
date = 2026-08-17T22:00:00+08:00
weight = 98
type = "docs"
description = "智能不安全代码 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/96_zh-cn.html](https://tourofrust.com/96_zh-cn.html)

# 智能不安全代码

智能指针倾向于经常使用*不安全*的代码。如前所述，它们是与 Rust 中最低级别的内存进行交互的常用工具。   
什么是不安全代码? 不安全代码的行为与普通 Rust 完全一样，除了一些 Rust 编译器无法保证的功能。    
不安全代码的主要功能是*解引用指针*。 这意味着将*原始指针*指向内存中的某个位置并声明“此处存在数据结构！” 并将其转换为您可以使用的数据表示（例如将`*const u8` 转换为`u8`）。 Rust 无法跟踪写入内存的每个字节的含义。
 因为 Rust 不能保证在用作 *指针* 的任意数字上存在什么，所以它将解引用放在一个 `unsafe { ... }` 块中。

智能指针广泛地被用来*解引用指针*，它们的作用得到了很好的证明。

## 示例代码

```rust
fn main() {
    let a: [u8; 4] = [86, 14, 73, 64];
    // this is a raw pointer. Getting the memory address
    // of something as a number is totally safe
    let pointer_a = &a as *const u8 as usize;
    println!("Data memory location: {}", pointer_a);
    // Turning our number into a raw pointer to a f32 is
    // also safe to do.
    let pointer_b = pointer_a as *const f32;
    let b = unsafe {
        // This is unsafe because we are telling the compiler
        // to assume our pointer is a valid f32 and
        // dereference it's value into the variable b.
        // Rust has no way to verify this assumption is true.
        *pointer_b
    };
    println!("I swear this is a pie! {}", b);
}
```
