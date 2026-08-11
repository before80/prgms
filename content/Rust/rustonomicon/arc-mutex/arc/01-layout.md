+++
title = "10.1.1 布局"
date = 2026-08-06T17:08:00+08:00
weight = 56
type = "docs"
description = "Arc 的布局"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 布局


> 原文链接: [https://doc.rust-lang.org/nomicon/arc-mutex/arc-layout.html](https://doc.rust-lang.org/nomicon/arc-mutex/arc-layout.html)


　　先为 `Arc` 实现确定布局。

　　`Arc<T>` 提供类型 `T` 值的线程安全共享所有权，分配在堆上。共享在 Rust 中意味着不可变，因此我们不必设计管理该值访问的机制，对吧？虽然 Mutex 等内部可变性类型允许 Arc 用户创造共享可变性，Arc 本身不必操心这些。

　　然而 Arc *确实*有一处必须考虑变更：销毁。当 Arc 的所有所有者都消失时，我们必须能 `drop` 其内容并释放分配。因此所有者需要知道自己是*最后一个*所有者，最简单的方式是计数——引用计数（Reference Counting）。

　　不幸的是，这个引用计数本质上是共享可变状态，所以 Arc *确实*要考虑同步。我们*可以*用 Mutex，但杀鸡用牛刀。改用原子操作。既然每个人都需要指向 T 分配的指针，不妨把引用计数放在同一分配里。

　　朴素地看，大致如下：

```rust
use std::sync::atomic;

pub struct Arc<T> {
    ptr: *mut ArcInner<T>,
}

pub struct ArcInner<T> {
    rc: atomic::AtomicUsize,
    data: T,
}
```

　　这能编译，但不正确。首先，编译器会给出过严的 variance（变型）。例如 `Arc<&'static str>` 无法用在需要 `Arc<&'a str>` 的地方。更重要的是，它会给 drop checker 错误的所有权信息，因为它会假设我们不拥有任何 `T` 类型的值。作为提供值共享所有权的结构，总会有某个实例完全拥有其数据。详见[所有权与 lifetime 一章](../ownership.md)中关于 variance 与 drop check 的全部细节。

　　为修复第一个问题，可用 `NonNull<T>`。注意 `NonNull<T>` 是对裸指针的包装，声明：

* 我们对 `T` 协变（covariant）
* 我们的指针永不为 null

　　为修复第二个问题，可加入包含 `ArcInner<T>` 的 `PhantomData` 标记。这会告诉 drop checker，我们对 `ArcInner<T>` 类型的值（其本身包含某个 `T`）有某种所有权概念。

　　经过这些改动，最终结构如下：

```rust
use std::marker::PhantomData;
use std::ptr::NonNull;
use std::sync::atomic::AtomicUsize;

pub struct Arc<T> {
    ptr: NonNull<ArcInner<T>>,
    phantom: PhantomData<ArcInner<T>>,
}

pub struct ArcInner<T> {
    rc: AtomicUsize,
    data: T,
}
```
