+++
title = "2.1 闭包语法"
date = 2026-08-11T11:30:00+08:00
weight = 97
type = "docs"
description = "01-闭包语法 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/closures/syntax.html](https://google.github.io/comprehensive-rust/closures/syntax.html)

# 2.1 闭包语法

闭包用竖线创建：`|..| ..`。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    // 参数与返回类型可推断，语法轻量：
    let double_it = |n| n * 2;
    dbg!(double_it(50));

    // 也可以指定类型并用花括号包住函数体，写得更显式：
    let add_1f32 = |x: f32| -> f32 { x + 1.0 };
    dbg!(add_1f32(50.));
}
```

> - 参数写在 `|..|` 之间。函数体可以用 `{ .. }` 包住；若是单个表达式，花括号可以省略。
>
> - 参数类型可选，未给出时会推断。返回类型也可选，但只有在用 `{ .. }` 包住函数体时才能写出。
>
> - 这两个例子也可以写成普通嵌套函数——它们没有从词法环境捕获任何变量。下一页会讲捕获。
>
> ## 深入探索
>
> - 能把函数存进变量的能力不只适用于闭包；普通函数也可以放进变量，再以与闭包相同的方式调用：[Playground 示例][fn-ptr]。
>
>   - 该示例还演示：不捕获任何东西的闭包也可以强制转换为普通函数指针。


[fn-ptr]: https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=817cbeeefc49f3d0d180a3d6d54c8bda
