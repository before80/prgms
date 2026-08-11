+++
title = "2.2 `Iterator` Trait"
date = 2026-08-11T11:30:00+08:00
weight = 164
type = "docs"
description = "02-`Iterator` Trait — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/iterators/iterator.html](https://google.github.io/comprehensive-rust/iterators/iterator.html)

# 2.2 `Iterator` Trait

[`Iterator`][1] trait 定义了如何用一个对象产出一串值。例如，若我们想创建一个能产出切片元素的迭代器，大致可以写成这样：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
struct SliceIter<'s> {
    slice: &'s [i32],
    i: usize,
}

impl<'s> Iterator for SliceIter<'s> {
    type Item = &'s i32;

    fn next(&mut self) -> Option<Self::Item> {
        if self.i == self.slice.len() {
            None
        } else {
            let next = &self.slice[self.i];
            self.i += 1;
            Some(next)
        }
    }
}

fn main() {
    let slice = &[2, 4, 6, 8];
    let iter = SliceIter { slice, i: 0 };
    for elem in iter {
        dbg!(elem);
    }
}
```

> - `SliceIter` 示例实现的逻辑与上一页演示的 C 风格 `for` 循环相同。
>
> - 向学员强调：迭代器是惰性的（lazy）。创建迭代器只是初始化结构体，不会立刻做任何工作；直到调用 `next` 方法才会真正开始。
>
> - 迭代器不必是有限的！完全可以写出永远产出值的迭代器。例如，半开区间 `0..` 会一直产生值，直到发生整数溢出。
>
> ## 更多探索
>
> - 「真正的」`SliceIter` 是标准库中的 [`slice::Iter`][2] 类型；真实实现底层用指针而非下标，以消除边界检查。
>
> - `SliceIter` 也是一个很好的例子：结构体包含引用，因此需要生命周期标注。
>
> - 你还可以演示给 `SliceIter` 加上泛型参数，使其适用于任意切片（而不只是 `&[i32]`）。


[1]: https://doc.rust-lang.org/std/iter/trait.Iterator.html
[2]: https://doc.rust-lang.org/stable/std/slice/struct.Iter.html
