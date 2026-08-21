+++
title = "10-枚举类型"
date = 2026-08-18T08:45:00+08:00
weight = 75
type = "docs"
description = "枚举类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types/enum.html](https://doc.rust-lang.org/reference/types/enum.html)

r[type.enum]
# 枚举类型

r[type.enum.intro]
*枚举类型*是指名的、异构的不相交并类型，由 [`enum` 项][`enum` item]的名称表示。[^enumtype]

r[type.enum.declaration]
[`enum` 项][`enum` item]同时声明该类型以及若干*变体*，每个变体都有独立的名称，语法分别对应结构体、元组结构体或类单元结构体。

r[type.enum.constructor]
可以用[结构体表达式][struct expression]构造 `enum` 的新实例。

r[type.enum.value]
任意 `enum` 值所占用的内存，等于其对应 `enum` 类型中最大变体的大小，再加上存储判别值所需的大小。

r[type.enum.name]
枚举类型不能以*结构*方式作为类型写出，而必须通过命名引用某个 [`enum` 项][`enum` item]来表示。

[^enumtype]: `enum` 类型类似于 Haskell 中的 `data` 构造函数声明，或 Limbo 中的 *pick ADT*。

[`enum` item]: ../items/enumerations.md
[struct expression]: ../expressions/struct-expr.md
