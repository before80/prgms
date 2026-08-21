+++
title = "14-指针类型"
date = 2026-08-18T08:45:00+08:00
weight = 79
type = "docs"
description = "指针类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types/pointer.html](https://doc.rust-lang.org/reference/types/pointer.html)

r[type.pointer]
# 指针类型

r[type.pointer.intro]
所有指针都是显式的一等值。它们可以被移动或复制，存入数据结构，以及从函数返回。

r[type.pointer.reference]
## 引用（`&` 和 `&mut`）

r[type.pointer.reference.syntax]
```grammar,types
ReferenceType -> `&` Lifetime? `mut`? TypeNoBounds
```

r[type.pointer.reference.shared]
### 共享引用（`&`）

r[type.pointer.reference.shared.intro]
共享引用指向由某个其他值所拥有的内存。

r[type.pointer.reference.shared.constraint-mutation]
当创建指向某个值的共享引用时，它会阻止对该值的直接修改。[内部可变性][Interior mutability]在某些情况下为此提供了例外。顾名思义，可以存在任意数量指向同一值的共享引用。共享引用类型写作 `&type`，或者在需要指定显式生命周期时写作 `&'a type`。

r[type.pointer.reference.shared.copy]
复制引用是一种「浅」操作：它只涉及复制指针本身，也就是说，指针是 `Copy` 的。释放引用对其所指向的值没有影响，但对[临时值][temporary value]的引用会在该引用自身的作用域内保持该临时值存活。

r[type.pointer.reference.mut]
### 可变引用（`&mut`）

r[type.pointer.reference.mut.intro]
可变引用指向由某个其他值所拥有的内存。可变引用类型写作 `&mut type` 或 `&'a mut type`。

r[type.pointer.reference.mut.copy]
可变引用（尚未被再借用的）是访问其所指向值的唯一方式，因此不是 `Copy` 的。

r[type.pointer.raw]
## 裸指针（`*const` 和 `*mut`）

r[type.pointer.raw.syntax]
```grammar,types
RawPointerType -> `*` ( `mut` | `const` ) TypeNoBounds
```

r[type.pointer.raw.intro]
裸指针是没有安全性或存活性保证的指针。裸指针写作 `*const T` 或 `*mut T`。例如 `*const i32` 表示指向 32 位整数的裸指针。

r[type.pointer.raw.copy]
复制或 drop 裸指针对任何其他值的生命周期都没有影响。

r[type.pointer.raw.safety]
解引用裸指针是一种 [`unsafe` 操作][`unsafe` operation]。

这也可以通过再借用（`&*` 或 `&mut *`）将裸指针转换为引用。一般不鼓励使用裸指针；它们的存在是为了支持与外部代码的互操作，以及编写性能关键或底层的函数。

r[type.pointer.raw.cmp]
比较裸指针时，比较的是它们的地址，而不是它们所指向的内容。比较指向[动态大小类型][dynamically sized types]的裸指针时，还会比较它们的附加数据。

r[type.pointer.raw.constructor]
裸指针可以直接使用 `&raw const` 创建 `*const` 指针，使用 `&raw mut` 创建 `*mut` 指针。

r[type.pointer.smart]
## 智能指针

标准库在引用和裸指针之外还包含额外的「智能指针」类型。

r[type.pointer.validity]
## 位有效性

r[type.pointer.validity.pointer-fragment]
尽管在大多数平台发出的机器码中，指针和引用类似于 `usize`，但将引用或指针类型 transmute 为非指针类型的语义目前尚未确定。因此，将指针或引用类型 `P` transmute 为 `[u8; size_of::<P>()]` 可能并不合法。

r[type.pointer.validity.raw]
对于瘦裸指针（即对于 `T: Sized`，`P = *const T` 或 `P = *mut T`），反向（将整数或整数数组 transmute 为 `P`）始终合法。然而，通过这种 transmute 产生的指针可能无法被解引用（即使 `T` 的[大小为零][size zero]也不行）。

[Interior mutability]: ../interior-mutability.md
[`unsafe` operation]: ../unsafety.md
[dynamically sized types]: ../dynamically-sized-types.md
[size zero]: glossary.zst
[temporary value]: ../expressions.md#temporaries
