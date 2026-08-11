+++
title = "第15章 智能指针"
date = 2026-08-05T08:44:00+08:00
weight = 67
type = "docs"
description = "指针、智能指针，以及 Box、Rc、RefCell 等标准库类型"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 智能指针 {#smart-pointers}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch15-00-smart-pointers.html](https://doc.rust-lang.org/stable/book/ch15-00-smart-pointers.html)


　　指针（pointer）是一个通用概念：变量里存放的是内存地址，该地址指向（或“指向”）另一处数据。Rust 中最常见的指针是引用（reference），你在第 4 章已经学过。引用用 `&` 符号表示，并借用它们所指向的值。除了引用数据之外，它们没有额外能力，也几乎没有开销。

　　另一方面，**智能指针**（smart pointer）是一类既像指针、又带有额外元数据与能力的数据结构。智能指针并非 Rust 独有：它起源于 C++，在其他语言中也存在。Rust 标准库定义了多种智能指针，提供的功能超出了引用。为了把握这一通用概念，我们会看几个不同的例子，其中包括**引用计数**（reference counting）智能指针：它通过跟踪所有者数量，让数据可以有多个所有者；当不再有任何所有者时，再清理数据。

　　在 Rust 中，由于所有权（ownership）与借用（borrowing）的概念，引用与智能指针还有一层区别：引用只是借用数据，而许多情况下智能指针**拥有**它们所指向的数据。

　　智能指针通常用结构体实现。与普通结构体不同，智能指针会实现 `Deref` 与 `Drop` 特征（trait）。`Deref` 让智能指针实例表现得像引用，这样你可以写出同时适用于引用和智能指针的代码。`Drop` 则允许你自定义智能指针实例离开作用域时要运行的代码。本章会讨论这两个特征，并说明它们对智能指针为何重要。

　　智能指针模式是 Rust 中常用的通用设计模式，本章不会覆盖所有现有的智能指针。许多库都有自己的智能指针，你甚至可以自己编写。我们会介绍标准库中最常见的几种：

- `Box<T>`，用于在堆上分配值
- `Rc<T>`，引用计数类型，支持多重所有权
- `Ref<T>` 与 `RefMut<T>`，通过 `RefCell<T>` 访问；该类型在运行时而非编译时强制执行借用规则

　　此外，我们还会介绍**内部可变性**（interior mutability）模式：不可变类型对外暴露修改内部值的 API。我们也会讨论引用循环：它们如何导致内存泄漏，以及如何避免。

　　开始吧！
