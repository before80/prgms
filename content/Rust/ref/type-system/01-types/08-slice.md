+++
title = "08-切片类型"
date = 2026-08-18T08:45:00+08:00
weight = 73
type = "docs"
description = "切片类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types/slice.html](https://doc.rust-lang.org/reference/types/slice.html)

r[type.slice]
# 切片类型

r[type.slice.syntax]
```grammar,types
SliceType -> `[` Type `]`
```

r[type.slice.intro]
切片是一种[动态大小类型][dynamically sized type]，表示对类型为 `T` 的元素序列的「视图」。切片类型写作 `[T]`。

r[type.slice.unsized]
切片类型通常通过指针类型使用。例如：

* `&[T]`：共享切片，常直接称为「切片」。它不拥有所指向的数据，而是借用它。
* `&mut [T]`：可变切片。它可变地借用所指向的数据。
* `Box<[T]>`：装箱切片

示例：

```rust
// 堆上分配的数组，被强制转换为切片
let boxed_array: Box<[i32]> = Box::new([1, 2, 3]);

// 指向数组的（共享）切片
let slice: &[i32] = &boxed_array[..];
```

r[type.slice.safe]
切片的所有元素总是已初始化，并且在安全方法和运算符中对切片的访问总是会进行边界检查。

[dynamically sized type]: ../dynamically-sized-types.md
