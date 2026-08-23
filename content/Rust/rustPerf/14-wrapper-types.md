+++
title = "14 包装类型"
date = 2026-08-23T13:57:00+08:00
weight = 15
type = "docs"
description = "Newtype 与透明包装"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Rust Performance Book](https://nnethercote.github.io/perf-book/)

# 包装类型 {#wrapper-types}


> 原文链接: [https://nnethercote.github.io/perf-book/wrapper-types.html](https://nnethercote.github.io/perf-book/wrapper-types.html)


Rust 有多种为值提供特殊行为的「包装」类型，例如 [`RefCell`] 和 [`Mutex`]。访问这些值可能花费可观时间。若多个此类值通常一起访问，把它们放在同一个包装里可能更好。

[`RefCell`]: https://doc.rust-lang.org/std/cell/struct.RefCell.html
[`Mutex`]: https://doc.rust-lang.org/std/sync/struct.Mutex.html

例如，下面这种结构：
```rust
# use std::sync::{Arc, Mutex};
struct S {
    x: Arc<Mutex<u32>>,
    y: Arc<Mutex<u32>>,
}
```
可能更适合表示为：
```rust
# use std::sync::{Arc, Mutex};
struct S {
    xy: Arc<Mutex<(u32, u32)>>,
}
```
这是否有助于性能取决于这些值的具体访问模式。
[**示例**](https://github.com/rust-lang/rust/pull/68694/commits/7426853ba255940b880f2e7f8026d60b94b42404)。
