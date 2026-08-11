+++
title = "4.4 Transmute"
date = 2026-08-06T17:08:00+08:00
weight = 26
type = "docs"
description = "mem::transmute 的危险与用法"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# Transmute


> 原文链接: [https://doc.rust-lang.org/nomicon/transmutes.html](https://doc.rust-lang.org/nomicon/transmutes.html)


　　让开，类型系统！我们要重新解释这些比特，不成功便成仁！尽管本书全是 unsafe 操作，我仍要再三强调：应深入思考本节操作之外的其他途径。这确实是 Rust 中最危险 unsafe 的操作之一。此处的护栏不过是牙线。

　　[`mem::transmute<T, U>`][transmute] 取 `T` 类型的值，将其重新解释为 `U` 类型。唯一限制是 `T` 和 `U` 须验证具有相同大小。用此函数制造未定义行为的方式令人眼花缭乱。

* 首要的是，用无效状态创建*任何*类型的实例都会导致无法真正预测的任意混乱。不要把 `3` transmute 成 `bool`。即使你永远不对 `bool` 做任何事。就是别这么干。

* `transmute` 有重载的返回类型。若不指定返回类型，可能为满足推断产生出乎意料的类型。

* 把 `&` transmute 成 `&mut` 是未定义行为。某些用法可能*看似* safe，但 Rust 优化器可假设共享引用在其生命周期内不会改变，此类 transmutation 会违背这些假设。因此：
  * 把 `&` transmute 成 `&mut` *永远*是未定义行为。
  * 你不能这么做。
  * 你并不特殊。

* transmute 成引用而未显式提供生命周期，会产生[无界生命周期]。

* 在不同复合类型之间 transmute 时，必须确保布局相同！若布局不同，错误字段会被填入错误数据，让你痛苦，也可能未定义行为（见上）。

　　  如何知道布局是否相同？对 `repr(C)` 和 `repr(transparent)` 类型，布局精确定义。但对普通的 `repr(Rust)` 则不是。甚至同一泛型类型的不同实例布局也可能截然不同。`Vec<i32>` 和 `Vec<u32>` 的字段*可能*顺序相同，也可能不同。数据布局究竟保证什么、不保证什么，[UCG WG][ucg-layout] 仍在完善。

　　[`mem::transmute_copy<T, U>`][transmute_copy] 比上面还更加危险。它从 `&T` 复制 `size_of<U>` 字节并解释为 `U`。`mem::transmute` 的大小检查没了（因为复制前缀可能合法），但若 `U` 大于 `T` 则是未定义行为。

　　当然，用裸指针 cast 或 `union` 也能实现这些函数的全部功能，但没有 lint 或其他基本健全性检查。裸指针 cast 和 `union` 同样无法规避上述规则。

[无界生命周期]: ../ownership/06-unbounded-lifetimes.html
[transmute]: ../std/mem/fn.transmute.html
[transmute_copy]: ../std/mem/fn.transmute_copy.html
[ucg-layout]: https://rust-lang.github.io/unsafe-code-guidelines/layout.html
