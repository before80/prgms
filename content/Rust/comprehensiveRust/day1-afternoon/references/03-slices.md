+++
title = "3.3 切片"
date = 2026-08-11T11:30:00+08:00
weight = 49
type = "docs"
description = "03-切片 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/references/slices.html](https://google.github.io/comprehensive-rust/references/slices.html)

# 3.3 切片

切片（slice）让你能查看更大集合中的一部分：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let a: [i32; 6] = [10, 20, 30, 40, 50, 60];
    println!("a: {a:?}");

    let s: &[i32] = &a[2..4];
    println!("s: {s:?}");
}
```

- 切片从被切片的类型借用数据。

> - 我们通过借用 `a`，并在方括号中指定起止下标来创建切片。
>
> - 若切片从下标 0 开始，Rust 的范围语法允许省略起始下标，因此 `&a[0..a.len()]` 与 `&a[..a.len()]` 相同。
>
> - 对最后一个下标也一样，因此 `&a[2..a.len()]` 与 `&a[2..]` 相同。
>
> - 要方便地创建覆盖整个数组的切片，可以用 `&a[..]`。
>
> - `s` 是指向 `i32` 切片的引用。注意 `s` 的类型（`&[i32]`）不再包含数组长度。这样我们就能对大小不同的切片做计算。
>
> - 切片总是从另一个对象借用。本例中，`a` 必须至少在切片存活期间保持“存活”（在作用域内）。
>
> - 切片一旦创建就不能“变大”：
>   - 不能往切片追加元素，因为它不拥有底层缓冲区。
>   - 也不能把切片扩大为指向底层缓冲区更大的一段。切片不知道底层缓冲区的长度，因此无法知道最多能扩到多大。
>   - 要得到更大的切片，必须回到原始缓冲区，再从那里创建更大的切片。

