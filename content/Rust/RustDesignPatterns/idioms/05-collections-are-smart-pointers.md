+++
title = "05-集合是智能指针"
date = 2026-08-18T22:10:00+08:00
weight = 9
type = "docs"
description = "集合是智能指针 — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/idioms/deref.html](https://rust-unofficial.github.io/patterns/idioms/deref.html)

# 集合是智能指针

## 描述 {#description}

使用 [`Deref`](https://doc.rust-lang.org/std/ops/trait.Deref.html) trait，
把集合当作智能指针来对待，从而提供数据的所有权视图和借用视图。

## 示例 {#example}

```rust,ignore
use std::ops::Deref;

struct Vec<T> {
    data: RawVec<T>,
    //..
}

impl<T> Deref for Vec<T> {
    type Target = [T];

    fn deref(&self) -> &[T] {
        //..
    }
}
```

`Vec<T>` 是 `T` 的所有权集合，而切片（`&[T]`）是 `T` 的借用集合。
为 `Vec` 实现 `Deref` 允许从 `&Vec<T>` 到 `&[T]` 的隐式解引用，
并把这种关系纳入自动解引用搜索。你可能期望为 `Vec` 实现的大多数方法，实际上是为切片实现的。

`String` 和 `&str` 也有类似关系。

## 动机 {#motivation}

所有权和借用是 Rust 语言的关键方面。数据结构必须妥善考虑这些语义，才能提供良好的用户体验。
在实现拥有其数据的数据结构时，提供该数据的借用视图可以带来更灵活的 API。

## 优点 {#advantages}

大多数方法可以只为借用视图实现，然后它们会隐式地可用于所有权视图。

让客户端可以选择借用数据还是取得数据的所有权。

## 缺点 {#disadvantages}

仅通过解引用才可用的方法和 trait 在约束检查时不会被考虑，因此使用此模式的数据结构做泛型编程时会变得复杂
（参见 `Borrow` 和 `AsRef` trait 等）。

## 讨论 {#discussion}

智能指针和集合是类比的：智能指针指向单个对象，而集合指向多个对象。从类型系统的角度看，
两者几乎没有区别。如果访问每个数据的唯一途径是通过该集合，并且集合负责删除这些数据
（即便在共享所有权的情况下，某种借用视图也可能是合适的），那么集合就拥有其数据。
如果集合拥有其数据，通常有用的做法是提供数据的借用视图，以便可以多次引用它。

大多数智能指针（例如 `Foo<T>`）实现 `Deref<Target=T>`。然而，集合通常会解引用到自定义类型。
`[T]` 和 `str` 有一些语言支持，但在一般情形下这并非必要。`Foo<T>` 可以实现 `Deref<Target=Bar<T>>`，
其中 `Bar` 是动态大小类型，而 `&Bar<T>` 是 `Foo<T>` 中数据的借用视图。

通常，有序集合会为 `Range` 实现 `Index` 以提供切片语法。目标类型将是借用视图。

## 参见 {#see-also}

- [Deref 多态反模式](../anti-patterns/03-deref-polymorphism/)。
- [`Deref` trait 文档](https://doc.rust-lang.org/std/ops/trait.Deref.html)。
