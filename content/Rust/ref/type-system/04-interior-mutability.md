+++
title = "04-内部可变性"
date = 2026-08-18T08:45:00+08:00
weight = 87
type = "docs"
description = "内部可变性 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/interior-mutability.html](https://doc.rust-lang.org/reference/interior-mutability.html)

r[interior-mut]
# 内部可变性

r[interior-mut.intro]
有时一个类型需要在存在多个别名的情况下被修改。在 Rust 中，这通过一种称为 _内部可变性_ 的模式来实现。

r[interior-mut.shared-ref]
若一个类型的内部状态可以通过指向它的[共享引用][shared reference]来改变，则该类型具有内部可变性。

r[interior-mut.no-constraint]
这与通常的[要求][ub]——共享引用所指向的值不得被修改——相悖。

r[interior-mut.unsafe-cell]
[`std::cell::UnsafeCell<T>`] 类型是允许关闭这一要求的唯一方式。当 `UnsafeCell<T>` 被不可变地别名时，修改其中包含的 `T`，或获取指向该 `T` 的可变引用，仍然是安全的。

r[interior-mut.mut-unsafe-cell]
与所有其他类型一样，同时存在多个 `&mut UnsafeCell<T>` 别名是未定义行为。

r[interior-mut.abstraction]
其他具有内部可变性的类型可以通过将 `UnsafeCell<T>` 用作字段来创建。标准库提供了多种提供安全内部可变性 API 的类型。

r[interior-mut.ref-cell]
例如，[`std::cell::RefCell<T>`] 使用运行时借用检查来确保围绕多重引用的通常规则。

r[interior-mut.atomic]
[`std::sync::atomic`] 模块包含一些类型，它们包装一个仅通过原子操作访问的值，从而允许该值在线程间共享并被修改。

[shared reference]: types/pointer.md#shared-references-
[ub]: behavior-considered-undefined.md
