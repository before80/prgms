+++
title = "4.2.2 Rust 为何没有继承？"
date = 2026-08-11T11:30:00+08:00
weight = 482
type = "docs"
description = "02-Rust 为何没有继承？— Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/why-no-inheritance.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/from-oop-to-rust/why-no-inheritance.html)

# 4.2.2 Rust 为何没有继承？

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub struct Id {
    pub id: u32
}

impl Id {
    // 方法
}

// 🔨❌，Rust 没有继承！
pub struct Data: Id {
    // 继承来的 "id" 字段
    pub name: String,
}

impl Data {
    // 方法，但也包含 Id 的方法，或者可能是对这些方法的覆盖。
}

// ✅
pub struct Data {
    pub id: Id,
    pub name: String,
}

impl Data {
    // Data 上所有非来自 trait 的方法。
}

impl SomeTrait for Data {
    // 在单独的 impl 块中为 trait 写实现。
}
```

> - 继承带来若干缺点。
>
> - 默认就是异构的：
>
>   类继承隐式允许不同类的类型互换使用，却无法指定具体类型，或判断某类型是否与另一类型相同。
>
>   对于相等或比较这类操作，这会导致比较与相等检查抛错或以其它方式 panic。
>
> - 数据结构由什么组成、如何行为，有多个「真相来源」：
>
>   类型的字段被继承层次遮蔽。
>
>   类型的方法可能覆盖父类型，也可能被子类型覆盖；在多方维护的复杂代码库中，很难看清一个类型真正的行为。
>
> - 默认使用动态分发，带来虚表（vtable）查找开销：
>
>   动态分发要工作，就需要某处存放「调用哪些方法」以及该类型其它运行时才知道的信息。
>
>   这个存放处就是值的 `vtable`。与编译期已知类型的方法调用相比，方法调用需要更多次解引用。

