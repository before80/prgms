+++
title = "2.1 动机"
date = 2026-08-11T11:30:00+08:00
weight = 163
type = "docs"
description = "01-动机 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/iterators/motivation.html](https://google.github.io/comprehensive-rust/iterators/motivation.html)

# 2.1 动机

若要遍历数组的内容，你需要定义：

- 一些状态，用来记录迭代进行到何处，例如一个下标。
- 一个条件，用来判断何时结束迭代。
- 每次循环更新迭代状态的逻辑。
- 利用该状态取出每个元素的逻辑。

在 C 风格的 `for` 循环中，这些内容是直接声明的：

```c,editable
for (int i = 0; i < array_len; i += 1) {
    int elem = array[i];
}
```

在 Rust 中，我们把这些状态与逻辑打包成一个对象，称为「迭代器」（iterator）。

> - 本页为下一页做铺垫：说明 Rust 迭代器在底层做了什么。我们用（希望）大家熟悉的 C 风格 `for` 循环，展示迭代需要状态与逻辑，这样下一页就能说明迭代器如何把它们打包在一起。
>
> - Rust 没有 C 风格的 `for` 循环，但可以用 `while` 表达同样的事情：
>   ```rust
>   // Copyright 2024 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   let array = [2, 4, 6, 8];
>   let mut i = 0;
>   while i < array.len() {
>       let elem = array[i];
>       i += 1;
>   }
>   ```
>
> ## 更多探索
>
> 在 C 和 C++ 里，还有另一种用 `for` 表达数组遍历的方式：用指向数组开头和末尾的指针，通过比较这两个指针来判断循环何时结束。
>
> ```c,editable
> for (int *ptr = array; ptr < array + len; ptr += 1) {
>     int elem = *ptr;
> }
> ```
>
> 若学员问起，可以指出：Rust 的切片（slice）与数组迭代器在底层就是这样工作的（当然仍实现为 Rust 迭代器）。

