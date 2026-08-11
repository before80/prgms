+++
title = "2.1 程序内存回顾"
date = 2026-08-11T11:30:00+08:00
weight = 124
type = "docs"
description = "01-程序内存回顾 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/memory-management/review.html](https://google.github.io/comprehensive-rust/memory-management/review.html)

# 2.1 程序内存回顾

程序以两种方式分配内存：

- 栈（Stack）：存放局部变量的连续内存区域。
  - 值的大小在编译期已知且固定。
  - 极快：只需移动栈指针。
  - 易于管理：随函数调用进出。
  - 内存局部性很好。

- 堆（Heap）：存放函数调用之外的值。
  - 值的大小在运行时动态确定。
  - 比栈稍慢：需要一些簿记开销。
  - 不保证内存局部性。

## 示例

创建 `String` 会把固定大小的元数据放在栈上，把动态大小的数据（实际字符串内容）放在堆上：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let s1 = String::from("Hello");
}
```

```bob
 Stack
.- - - - - - - - - - - - - -.      Heap
:                           :     .- - - - - - - - - - - - - - - -.
:    s1                     :     :                               :
:   +-----------+-------+   :     :                               :
:   | capacity  |     5 |   :     :   +----+----+----+----+----+  :
:   | ptr       |     o-+---+-----+-->| H  | e  | l  | l  | o  |  :
:   | len       |     5 |   :     :   +----+----+----+----+----+  :
:   +-----------+-------+   :     :                               :
:                           :     :                               :
`- - - - - - - - - - - - - -'     `- - - - - - - - - - - - - - - -'
```

> - 可以提到：`String` 底层由 `Vec` 支撑，因此有 capacity 与 length；若可变，可通过在堆上重新分配来增长。
>
> - 若学员问起，可说明底层内存由 [System Allocator] 在堆上分配，也可通过 [Allocator API] 实现自定义分配器。
>
> ## 延伸阅读
>
> 可以用 `unsafe` Rust 查看内存布局。但务必强调：这样做本身就是不安全的！
>
> ```rust
> // Copyright 2023 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> fn main() {
>     let mut s1 = String::from("Hello");
>     s1.push(' ');
>     s1.push_str("world");
>     // 切勿在生产代码中这样做！仅用于教学演示。
>     // String 不保证其布局，这样做可能导致未定义行为。
>     unsafe {
>         let (capacity, ptr, len): (usize, usize, usize) = std::mem::transmute(s1);
>         println!("capacity = {capacity}, ptr = {ptr:#x}, len = {len}");
>     }
> }
> ```


[System Allocator]: https://doc.rust-lang.org/std/alloc/struct.System.html
[Allocator API]: https://doc.rust-lang.org/std/alloc/index.html
