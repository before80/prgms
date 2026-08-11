+++
title = "2.5 `IntoIterator`"
date = 2026-08-11T11:30:00+08:00
weight = 167
type = "docs"
description = "05-`IntoIterator` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/iterators/intoiterator.html](https://google.github.io/comprehensive-rust/iterators/intoiterator.html)

# 2.5 `IntoIterator`

`Iterator` trait 告诉你：一旦有了迭代器，该如何*迭代*。相关的
[`IntoIterator`](https://doc.rust-lang.org/std/iter/trait.IntoIterator.html)
trait 则定义了如何为某个类型创建迭代器。它会被 `for` 循环自动使用。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
struct Grid {
    x_coords: Vec<u32>,
    y_coords: Vec<u32>,
}

impl IntoIterator for Grid {
    type Item = (u32, u32);
    type IntoIter = GridIter;
    fn into_iter(self) -> GridIter {
        GridIter { grid: self, i: 0, j: 0 }
    }
}

struct GridIter {
    grid: Grid,
    i: usize,
    j: usize,
}

impl Iterator for GridIter {
    type Item = (u32, u32);

    fn next(&mut self) -> Option<(u32, u32)> {
        if self.i >= self.grid.x_coords.len() {
            self.i = 0;
            self.j += 1;
            if self.j >= self.grid.y_coords.len() {
                return None;
            }
        }
        let res = Some((self.grid.x_coords[self.i], self.grid.y_coords[self.j]));
        self.i += 1;
        res
    }
}

fn main() {
    let grid = Grid { x_coords: vec![3, 5, 7, 9], y_coords: vec![10, 20, 30, 40] };
    for (x, y) in grid {
        println!("point = {x}, {y}");
    }
}
```

> - `IntoIterator` 正是让 `for` 循环得以工作的 trait。诸如 `Vec<T>` 以及它们的引用（如 `&Vec<T>` 和 `&[T]`）都实现了它；区间（range）也实现了它。因此你可以写 `for i in some_vec { .. }` 来遍历向量，但 `some_vec.next()` 并不存在。
>
> 点开 `IntoIterator` 的文档。每个 `IntoIterator` 实现都必须声明两个类型：
>
> - `Item`：要迭代的元素类型，例如 `i8`，
> - `IntoIter`：`into_iter` 方法返回的 `Iterator` 类型。
>
> 注意 `IntoIter` 与 `Item` 是关联的：该迭代器必须具有相同的 `Item` 类型，也就是说它返回 `Option<Item>`。
>
> 本示例遍历所有 x、y 坐标的组合。
>
> 试着在 `main` 里对 `grid` 迭代两次。为什么会失败？注意 `IntoIterator::into_iter` 会取得 `self` 的所有权。
>
> 修复方法：为 `&Grid` 实现 `IntoIterator`，并创建一个按引用迭代的 `GridRefIter`。同时包含 `GridIter` 与 `GridRefIter` 的版本见[此 playground][1]。
>
> 标准库类型也会遇到同样的问题：`for e in some_vector` 会取得 `some_vector` 的所有权，并迭代其中的自有元素。应改用 `for e in &some_vector`，以迭代元素的引用。


[1]: https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=947e371c7295af758504f01f149023a1
