+++
title = "11-联合体类型"
date = 2026-08-18T08:45:00+08:00
weight = 76
type = "docs"
description = "联合体类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types/union.html](https://doc.rust-lang.org/reference/types/union.html)

r[type.union]
# 联合体类型

r[type.union.intro]
*联合体类型*是指名的、异构的类 C 联合体，由 [`union` 项][item]的名称表示。

r[type.union.access]
联合体没有「活动字段」的概念。相反，每一次联合体访问都会把联合体内容的一部分 transmute 为所访问字段的类型。

r[type.union.safety]
由于 transmute 可能导致意外或未定义行为，从联合体字段读取需要 `unsafe`。

r[type.union.constraint]
联合体字段类型也被限制为某一类型子集，以保证它们永远不需要析构。更多细节见该项的[文档][item]。

r[type.union.layout]
默认情况下 `union` 的内存布局未定义（特别地，字段*不必*位于偏移 0），但可以用 `#[repr(...)]` 属性固定布局。

[`Copy`]: ../special-types-and-traits.md#copy
[item]: ../items/unions.md
