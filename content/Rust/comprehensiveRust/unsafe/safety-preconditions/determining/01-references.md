+++
title = "4.3.1 示例：引用"
date = 2026-08-11T11:30:00+08:00
weight = 522
type = "docs"
description = "01-示例：引用 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/safety-preconditions/references.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/safety-preconditions/references.html)

# 4.3.1 示例：引用

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let mut boxed = Box::new(123);
    let a: *mut i32 = &mut *boxed as *mut i32;
    let b: *mut i32 = std::ptr::null_mut();

    println!("{:?}", *a);
    println!("{:?}", b.as_mut());
}
```

确认对语法的理解

- `Box<i32>` 类型是对堆上整数的引用，由 box 拥有。
- `*mut i32` 类型是所谓的原始指针（raw pointer），指向编译器不知道所有权的整数。程序员需要在无编译器协助的情况下自行保证规则。
  - 注意：原始指针不向 Rust 提供所有权信息。指针在语义上可以拥有数据，也可以借用数据，但该信息只存在于程序员的头脑中。

- `&mut *boxed as *mut _` 表达式：
  - `*boxed` 是……
  - `&mut *boxed` 是……
  - 最后，`as *mut i32` 将引用转换为指针。

- 引用（如 `&mut i32`）会「借用」（borrow）其指向的对象。这是 Rust 的所有权（ownership）系统。

确认对所有权（ownership）的理解

- 逐步讲解代码：
  - （第 3 行）通过解引用 box、创建新引用并将该引用转换为指针，得到指向 `123` 的原始指针。
  - （第 4 行）创建值为 NULL 的原始指针
  - （第 7 行）用 `.as_mut()` 将原始指针转换为 `Option`

- 强调 Rust 中的指针可以为 null（与引用不同）。

- 编译以查看错误信息。

- 讨论
  - （第 6 行）`println!("{:?}", *a);`
    - 前缀 `*` 解引用原始指针。
    - 这是显式操作。而普通引用大多时候得益于 `Deref` trait 会隐式解引用。这称为「自动解引用」（auto-deref）。
    - 解引用原始指针是不安全操作。
    - 需要 `unsafe` 块。
  - （第 7 行）`println!("{:?}", b.as_mut());`
    - `as_mut()` 是不安全函数。
    - 调用不安全函数需要 `unsafe` 块。

- 演示：修复代码（添加 `unsafe` 块）并再次编译，展示可运行的程序。

- 演示：将 `as *mut i32` 替换为 `as *mut _`，说明可以编译。

  - 我们可以在类型转换中部分省略目标类型。Rust 编译器知道转换源是 `&mut i32`。该引用类型只能转换为一种指针类型 `*mut i32`。

- 添加 SAFETY 注释：
  - 我们说 `unsafe` 代码标志着责任从编译器转移到程序员。
  - 如何表明我们在编写 `unsafe` 代码时已考虑这些特殊责任？SAFETY 注释。
  - SAFETY 注释解释 `unsafe` 代码为何正确。
  - 没有 SAFETY 注释，`unsafe` 代码就不安全。

- 讨论：使用一个大 `unsafe` 块还是两个较小的块：
  - 可以使用单个 `unsafe` 块，而不是多个。
  - 使用多个块可以让 SAFETY 注释尽可能具体。

[ptr-as_mut]: https://doc.rust-lang.org/stable/std/primitive.pointer.html#method.as_mut

_建议解法_

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let mut boxed = Box::new(123);
    let a: *mut i32 = &mut *boxed as *mut i32;
    let b: *mut i32 = std::ptr::null_mut();

    // SAFETY：`a` 是指向 i32 的非 null 指针，已初始化且仍在分配中。
    println!("{:?}", unsafe { *a });

    // SAFETY：`b` 是 null 指针，`as_mut()` 会将其转换为 `None`。
    println!("{:?}", unsafe { b.as_mut() });
}
```
