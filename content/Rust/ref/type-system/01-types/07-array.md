+++
title = "07-数组类型"
date = 2026-08-18T08:45:00+08:00
weight = 72
type = "docs"
description = "数组类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types/array.html](https://doc.rust-lang.org/reference/types/array.html)

r[type.array]
# 数组类型

r[type.array.syntax]
```grammar,types
ArrayType -> `[` Type `;` Expression `]`
```

r[type.array.intro]
数组是 `N` 个类型为 `T` 的元素组成的固定大小序列。数组类型写作 `[T; N]`。

r[type.array.constraint]
大小是求值为 [`usize`] 的[常量表达式][constant expression]。

示例：

```rust
// 栈上分配的数组
let array: [i32; 3] = [1, 2, 3];

// 堆上分配的数组，被强制转换为切片
let boxed_array: Box<[i32]> = Box::new([1, 2, 3]);
```

r[type.array.index]
数组的所有元素总是已初始化，并且在安全方法和运算符中对数组的访问总是会进行边界检查。

> **注意**
> 标准库类型 [`Vec<T>`] 提供堆上分配的可变大小数组类型。

[`usize`]: numeric.md#machine-dependent-integer-types
[constant expression]: ../const_eval.md#constant-expressions
