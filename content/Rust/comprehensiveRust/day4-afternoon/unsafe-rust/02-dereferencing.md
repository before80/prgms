+++
title = "3.2 解引用裸指针"
date = 2026-08-11T11:30:00+08:00
weight = 198
type = "docs"
description = "02-解引用裸指针 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-rust/dereferencing.html](https://google.github.io/comprehensive-rust/unsafe-rust/dereferencing.html)

# 3.2 解引用裸指针

创建指针是安全的，但解引用它们需要 `unsafe`：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let mut x = 10;

    let p1: *mut i32 = &raw mut x;
    let p2 = p1 as *const i32;

    // SAFETY: p1 与 p2 通过对局部变量取裸指针得到，因此保证非空、对齐，
    // 并且指向同一个（栈上）已分配对象。
    //
    // 裸指针所指向的对象在整个函数期间都存活，因此在裸指针仍存在时不会被释放。
    // 存在裸指针期间不会通过引用访问该对象，也不会从其他线程并发访问。
    unsafe {
        dbg!(*p1);
        *p1 = 6;
        // 通过裸指针观察突变在语义上是合理的，就像在 C 中一样。
        dbg!(*p2);
    }

    // 不健全（UNSOUND）。不要这样做。
    /*
    let r: &i32 = unsafe { &*p1 };
    dbg!(r);
    x = 50;
    dbg!(r); // 引用所指向的对象已被修改。这是未定义行为（UB）。
    */
}
```

> <summary>讲师备注</summary>
>
> 良好实践（也是 Android Rust 风格指南的要求）是为每个 `unsafe` 块写注释，说明其中的代码如何满足所做 unsafe 操作的安全要求。
>
> 就指针解引用而言，这意味着指针必须是
> [_valid_（有效的）](https://doc.rust-lang.org/std/ptr/index.html#safety)，即：
>
> - 指针必须非空。
> - 指针必须可解引用（位于单个已分配对象的边界内）。
> - 对象不得已被释放。
> - 不得存在对同一位置的并发访问。
> - 若指针由引用转换而来，底层对象必须仍存活，且不得再通过引用来访问该内存。
>
> 多数情况下，指针还必须正确对齐。
>
> “UNSOUND” 一节给出了一类常见 UB bug 的例子：天真地对裸指针的解引用结果取引用，会绕过编译器对该引用实际指向哪个对象的认知。因此借用检查器不会“冻结” `x`，我们就能在仍存在对其引用的情况下修改它。从指针创建引用需要格外小心。

