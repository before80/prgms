+++
title = "9.1 布局"
date = 2026-08-06T17:08:00+08:00
weight = 43
type = "docs"
description = "Vec 的内存布局"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 布局


> 原文链接: [https://doc.rust-lang.org/nomicon/vec/vec-layout.html](https://doc.rust-lang.org/nomicon/vec/vec-layout.html)


　　首先，我们需要确定 struct 布局。`Vec` 有三部分：指向分配的指针、分配的大小、已初始化元素的数量。

　　直观上，我们只需这种设计：

```rust,ignore
pub struct Vec<T> {
    ptr: *mut T,
    cap: usize,
    len: usize,
}
```

　　这确实能编译。不幸的是，它会过于严格。编译器会给出过于严格的 variance。于是 `&Vec<&'static str>` 不能用在需要 `&Vec<&'a str>` 的地方。详见[所有权与 lifetime 章节][ownership]。

　　如所有权章所见，标准库在拥有分配时用 `Unique<T>` 代替 `*mut T`。`Unique` 不稳定，因此我们尽可能不用。

　　简要回顾，`Unique` 是围绕 raw pointer 的包装，声明：

* 我们对 `T` 是协变的（covariant）
* 我们可能拥有类型 `T` 的值（与此例无关，但见 [PhantomData 章节][phantom-data] 了解真实 `std::vec::Vec<T>` 为何需要）
* 若 `T` 是 Send/Sync，则我们是 Send/Sync
* 我们的指针永不为 null（因此 `Option<Vec<T>>` 是 null 指针优化）

　　我们可以在稳定 Rust 中实现上述全部要求。为此，不用 `Unique<T>`，而用 [`NonNull<T>`][NonNull]——另一个 raw pointer 包装，给我们上述性质中的两条：对 `T` 协变，且声明永不为 null。若 `T` 是 Send/Sync 则实现 Send/Sync，效果与 `Unique<T>` 相同：

```rust
use std::ptr::NonNull;

pub struct Vec<T> {
    ptr: NonNull<T>,
    cap: usize,
    len: usize,
}

unsafe impl<T: Send> Send for Vec<T> {}
unsafe impl<T: Sync> Sync for Vec<T> {}
# fn main() {}
```

[ownership]: ../ownership.html
[phantom-data]: ../phantom-data.md
[NonNull]: ../../std/ptr/struct.NonNull.html
