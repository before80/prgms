+++
title = "2.1 数组"
date = 2026-08-11T11:30:00+08:00
weight = 40
type = "docs"
description = "01-数组 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/tuples-and-arrays/arrays.html](https://google.github.io/comprehensive-rust/tuples-and-arrays/arrays.html)

# 2.1 数组

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let mut a: [i8; 5] = [5, 4, 3, 2, 1];
    a[2] = 0;
    println!("a: {a:?}");
}
```

> - 数组也可以用简写语法初始化，例如 `[0; 1024]`。当你希望所有元素设为同一值，或数组很大、手工初始化不便时，这很有用。
>
> - 数组类型 `[T; N]` 的值包含 `N` 个（编译期常量）同类型 `T` 的元素。注意长度是类型的**一部分**，因此 `[u8; 3]` 与 `[u8; 4]` 是两种不同的类型。长度在运行时确定的切片（slice）稍后再讲。
>
> - 试着访问越界的数组元素。编译器能判断该下标不安全，因而不会编译通过：
>
> ```rust
> // Copyright 2024 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> fn main() {
>     let mut a: [i8; 5] = [5, 4, 3, 2, 1];
>     a[6] = 0;
>     println!("a: {a:?}");
> }
> ```
>
> - 数组访问会在运行时检查。Rust 在可能时会优化掉这些检查：若编译器能证明访问安全，就会去掉运行时检查以提升性能。也可以用 unsafe Rust 绕过检查。这种优化很强，很难给出运行时检查失败的例子。下面代码能编译，但会在运行时 panic：
>
> ```rust
> // Copyright 2024 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> fn get_index() -> usize {
>     6
> }
>
> fn main() {
>     let mut a: [i8; 5] = [5, 4, 3, 2, 1];
>     a[get_index()] = 0;
>     println!("a: {a:?}");
> }
> ```
>
> - 我们可以用字面量给数组赋值。
>
> - 数组不是堆分配的。它们是大小在编译期已知的普通值，因此放在栈上。若学员来自默认把数组放在堆上的垃圾回收语言，这可能出乎意料。
>
> - 无法从数组中删除或添加元素。数组长度在编译期固定，运行时不能改变。
>
> ## 调试打印
>
> - `println!` 宏通过 `?` 格式参数请求调试实现：`{}` 给出默认输出，`{:?}` 给出调试输出。整数和字符串等类型实现了默认输出，但数组只实现了调试输出，因此这里必须使用调试输出。
>
> - 加上 `#`，例如 `{a:#?}`，会启用“美化打印”格式，通常更易读。

