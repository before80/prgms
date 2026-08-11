+++
title = "2.1 不可失败模式"
date = 2026-08-11T11:30:00+08:00
weight = 66
type = "docs"
description = "01-不可失败模式 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/pattern-matching/infallible.html](https://google.github.io/comprehensive-rust/pattern-matching/infallible.html)

# 2.1 不可失败模式

第 1 天我们简要看过如何用模式_解构_（destructure）复合值。下面复习一下，并介绍模式还能表达的其他内容：

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn takes_tuple(tuple: (char, i32, bool)) {
    let a = tuple.0;
    let b = tuple.1;
    let c = tuple.2;

    // 与上面效果相同。
    let (a, b, c) = tuple;

    // 忽略第一个元素，只绑定第二、三个。
    let (_, b, c) = tuple;

    // 忽略除最后一个以外的所有元素。
    let (.., c) = tuple;
}

fn main() {
    takes_tuple(('a', 777, true));
}
```

> - 以上演示的模式都是_不可失败的_（irrefutable），即总会匹配右侧的值。
>
> - 模式是类型相关的，不可失败模式也是如此。试着给元组增减一个元素，观察编译器报错。
>
> - 变量名本身也是模式：总会匹配，并把匹配到的值绑定到同名新变量。
>
> - `_` 是总会匹配任意值并丢弃该值的模式。
>
> - `..` 允许一次忽略多个值。
>
> ## 深入探索
>
> - 还可以演示 `..` 的更多用法，例如忽略元组中间的元素。
>
>   ```rust
>   // Copyright 2025 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   fn takes_tuple(tuple: (char, i32, bool, u8)) {
>       let (first, .., last) = tuple;
>   }
>   ```
>
> - 这些模式对数组同样适用：
>
>   ```rust
>   // Copyright 2025 Google LLC
>   // SPDX-License-Identifier: Apache-2.0
>   #
>   fn takes_array(array: [u8; 5]) {
>       let [first, .., last] = array;
>   }
>   ```

