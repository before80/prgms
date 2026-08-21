+++
title = "03-不视为不安全的行为"
date = 2026-08-18T08:45:00+08:00
weight = 111
type = "docs"
description = "不视为不安全的行为 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/behavior-not-considered-unsafe.html](https://doc.rust-lang.org/reference/behavior-not-considered-unsafe.html)

# 不视为不安全的行为

Rust 编译器不认为下列行为是_不安全_的，尽管程序员可能（也应该）觉得它们不受欢迎、出乎意料或是错误的。

- 死锁
- 内存及其他资源泄漏
- 未调用析构函数就退出
- 通过指针泄漏暴露随机化的基地址

## 整数溢出

若程序包含算术溢出，则程序员犯了错误。在下文讨论中，我们区分算术溢出与回绕算术。前者是错误的，后者是有意为之。

当程序员启用了 `debug_assert!` 断言（例如通过启用非优化构建）时，实现必须插入动态检查，在溢出时 `panic`。其他类型的构建在溢出时可能 `panic`，也可能静默得到回绕后的值，由实现自行决定。

在隐式回绕溢出的情况下，实现必须通过使用二进制补码溢出约定，提供定义良好的结果（即便仍被视为错误）。

整型提供固有方法，使程序员能够显式执行回绕算术。例如，`i32::wrapping_add` 提供二进制补码回绕加法。

标准库还提供 `Wrapping<T>` newtype，确保 `T` 的所有标准算术运算都具有回绕语义。

关于整数溢出的错误条件、设计理由及更多细节，见 [RFC 560]。

## 逻辑错误

安全代码可能施加既无法在编译期也无法在运行时检查的额外逻辑约束。若程序违反此类约束，行为可能未指明，但不会导致未定义行为。这可能包括 panic、错误结果、中止以及不终止。行为也可能因运行、构建或构建种类而异。

例如，同时实现 `Hash` 与 `Eq` 要求被视为相等的值具有相等的哈希。另一个例子是 `BinaryHeap`、`BTreeMap`、`BTreeSet`、`HashMap` 和 `HashSet` 这类数据结构，它们描述了在键位于数据结构中时对其修改的约束。违反此类约束不被视为不安全，但程序被视为错误的，其行为不可预测。

[RFC 560]: https://github.com/rust-lang/rfcs/blob/master/text/0560-integer-overflow.md
