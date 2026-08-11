+++
title = "2.6 Copy 类型"
date = 2026-08-11T11:30:00+08:00
weight = 129
type = "docs"
description = "06-Copy 类型 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/memory-management/copy-types.html](https://google.github.io/comprehensive-rust/memory-management/copy-types.html)

# 2.6 Copy 类型

虽然移动语义是默认行为，但某些类型默认会拷贝：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let x = 42;
    let y = x;
    dbg!(x); // would not be accessible if not Copy
    dbg!(y);
}
```

这些类型实现了 `Copy` trait。

你可以选择让自己的类型使用拷贝语义：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Copy, Clone, Debug)]
struct Point(i32, i32);

fn main() {
    let p1 = Point(3, 4);
    let p2 = p1;
    println!("p1: {p1:?}");
    println!("p2: {p2:?}");
}
```

- 赋值之后，`p1` 与 `p2` 各自拥有自己的数据。
- 也可以用 `p1.clone()` 显式拷贝数据。

> 拷贝（Copy）与克隆（Clone）不是一回事：
>
> - 拷贝指对内存区域的按位复制，不能用于任意对象。
> - 拷贝不允许自定义逻辑（与 C++ 的拷贝构造函数不同）。
> - 克隆是更通用的操作，也可通过实现 `Clone` trait 自定义行为。
> - 实现了 `Drop` trait 的类型不能实现 `Copy`。
>
> 在上面的例子中，可以尝试：
>
> - 给 `struct Point` 加一个 `String` 字段。将无法编译，因为 `String` 不是 `Copy` 类型。
> - 从 `derive` 属性中去掉 `Copy`。编译错误会转移到针对 `p1` 的 `println!`。
> - 展示若改为克隆 `p1` 则可以工作。
>
> # 延伸阅读
>
> - 共享引用是 `Copy`/`Clone` 的，可变引用则不是。因为 Rust 要求可变引用独占，所以复制共享引用合法，而复制可变引用会违反借用规则。

