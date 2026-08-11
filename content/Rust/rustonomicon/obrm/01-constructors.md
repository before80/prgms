+++
title = "6.1 构造函数"
date = 2026-08-06T17:08:00+08:00
weight = 32
type = "docs"
description = "Rust 中的构造模式"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 构造函数


> 原文链接: [https://doc.rust-lang.org/nomicon/constructors.html](https://doc.rust-lang.org/nomicon/constructors.html)


　　创建用户定义类型实例有且仅有一种方式：命名它，并一次性初始化所有字段：

```rust
struct Foo {
    a: u8,
    b: u32,
    c: bool,
}

enum Bar {
    X(u32),
    Y(bool),
}

struct Unit;

let foo = Foo { a: 0, b: 1, c: false };
let bar = Bar::X(0);
let empty = Unit;
```

　　就这些。创建类型实例的其他一切方式，都只是调用做一些事情的普通函数，最终归结于**唯一真正的构造方式**。

　　与 C++ 不同，Rust 没有一整套内置构造种类。
　　没有 Copy、Default、Assignment、Move 等构造函数。原因各异，但主要归结于 Rust 强调*显式*的哲学。

　　Move 构造函数在 Rust 中没有意义，因为我们不让类型「关心」自己在内存中的位置。每种类型都必须准备好被盲目 memcpy 到内存别处。这意味着纯栈上但仍可 move 的侵入式（intrusive）链表在 Rust 中安全地基本不可能。

　　赋值和 copy 构造函数同样不存在，因为 move 语义是 Rust 中唯一的语义。至多 `x = y` 只是把 y 的比特 move 进 x 变量。Rust 提供两种设施实现 C++ 的 copy 导向语义：`Copy` 和 `Clone`。Clone 在概念上相当于 copy 构造函数，但从不隐式调用。须显式对要 clone 的元素调用 `clone`。Copy 是 Clone 的特殊情况，实现就是「复制比特」。Copy 类型被 move 时*会*隐式 clone，但按 Copy 的定义这只是不把旧副本当未初始化——空操作。

　　Rust 提供 `Default` trait 指定概念上的 default 构造函数，但此 trait 极少被使用。
　　这是因为变量[不会隐式初始化][uninit]。Default 基本上只对泛型编程有用。在具体上下文中，类型会提供静态 `new` 方法作为各种「默认」构造函数。这与其他语言的 `new` 无关，没有特殊含义。只是命名约定。

　　TODO: 讨论「placement new」？

[uninit]: ../uninitialized/_index.html
