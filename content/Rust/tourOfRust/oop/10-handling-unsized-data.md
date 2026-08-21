+++
title = "10-处理未知大小的数据"
date = 2026-08-17T22:00:00+08:00
weight = 85
type = "docs"
description = "处理未知大小的数据 — Rust 语言之旅"
isCJKLanguage = true
draft = false
+++

> 内容来源 · [Tour of Rust / Rust 语言之旅](https://github.com/richardanaya/tour_of_rust)

> 原文链接: [https://tourofrust.com/83_zh-cn.html](https://tourofrust.com/83_zh-cn.html)

# 处理未知大小的数据

当我们想把 Trait 存储在另一个结构中时，它们亦带来了一个有趣的挑战。 Trait 混淆了原始结构，因此它也混淆了原来的结构体的大小。在 Rust 中，在结构体中存储未知大小的值有两种处理方式。

* `泛型（generics）`——使用参数化类型创建已知类型的结构/函数，因此大小变成已知的。
* `间接存储（indirection）`——将实例放在堆上，给我们提供了一个间接的层次，让我们不必担心实际类型的大小，只需存储一个指向它的指针。不过还有其他方法！
