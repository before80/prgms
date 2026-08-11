+++
title = "2.4.2 `RefCell`"
date = 2026-08-11T11:30:00+08:00
weight = 147
type = "docs"
description = "02-`RefCell` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/borrowing/interior-mutability/refcell.html](https://google.github.io/comprehensive-rust/borrowing/interior-mutability/refcell.html)

# 2.4.2 `RefCell`

`RefCell` 允许访问并修改被包装的值，方式是提供模拟 `&T`/`&mut T`、但并非真正 Rust 引用的替代类型 `Ref` 与 `RefMut`。

这些类型使用 `RefCell` 中的计数器进行动态检查，防止 `RefMut` 与另一个 `Ref`/`RefMut` 同时存在。

通过实现 `Deref`（以及 `RefMut` 的 `DerefMut`），这些类型允许在内部值上调用方法，同时不允许引用逃逸。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::cell::RefCell;

fn main() {
    // 注意：`cell` 并未声明为可变。
    let cell = RefCell::new(5);

    {
        let mut cell_ref = cell.borrow_mut();
        *cell_ref = 123;

        // 这会在运行时触发错误。
        // let other = cell.borrow();
        // println!("{}", other);
    }

    println!("{cell:?}");
}
```

> - `RefCell` 用运行时检查强制执行 Rust 通常的借用规则（要么多个共享引用，要么单个独占引用）。在本例中，所有借用都很短且从不重叠，因此检查总是成功。
>
> - 例子中的额外代码块是为了在打印 cell 之前结束由 `borrow_mut` 创建的借用。试图打印仍被借用的 `RefCell` 只会显示 `"{borrowed}"`。
>
> ## 延伸阅读
>
> 还有 `OnceCell` 与 `OnceLock`，允许首次使用时初始化。要有效使用它们，需要学员目前尚不具备的更多知识。

