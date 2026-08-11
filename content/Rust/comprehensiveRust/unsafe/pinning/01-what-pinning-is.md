+++
title = "8.1 什么是 pinning"
date = 2026-08-11T11:30:00+08:00
weight = 547
type = "docs"
description = "01-什么是 pinning — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/what-pinning-is.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/pinning/what-pinning-is.html)

# 8.1 什么是 pinning

- 被固定的类型不能改变其内存地址（移动）
- 被指向的值不能被 safe 代码移动

`Pin<Ptr>` 利用所有权系统来控制如何访问被固定的值。Rust 并未改变语言本身，而是通过所有权系统来强制 pinning。`Pin` 拥有其内容，且其 safe API 中没有任何操作会触发移动。

这一点将在后续讲解

> 从概念上讲，pinning 阻止了默认的移动行为。
>
> 这看起来像是语言本身的改变。
>
> 然而，`Pin` 包装器实际上并未改变语言的任何根本特性。
>
> `Pin` 不暴露允许移动的 safe API，因此它可以阻止按位拷贝。
>
> unsafe API 允许库作者包装未实现 `Unpin` 的类型，但他们必须维护相同的保证。
>
> `Pin` 的文档使用术语「pointer types（指针类型）」。
>
> 「指针类型」比语言中的指针原始类型含义更广。
>
> 「指针类型」指实现了 `Deref`、且其 `Target` 实现了 `Unpin` 的任意类型。
>
> Rust 风格说明：这一 trait 约束通过 `::new()` 构造函数的 trait 边界来强制，而非约束类型本身。

