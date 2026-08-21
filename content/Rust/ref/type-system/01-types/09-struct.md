+++
title = "09-结构体类型"
date = 2026-08-18T08:45:00+08:00
weight = 74
type = "docs"
description = "结构体类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types/struct.html](https://doc.rust-lang.org/reference/types/struct.html)

r[type.struct]
# 结构体类型

r[type.struct.intro]
`struct` *类型*是其他类型的异构积，这些其他类型称为该类型的*字段*。[^structtype]

r[type.struct.constructor]
可以用[结构体表达式][struct expression]构造 `struct` 的新实例。

r[type.struct.layout]
默认情况下 `struct` 的内存布局未定义，以便编译器可以进行字段重排等优化，但可以用 [`repr` 属性][`repr` attribute]固定布局。无论哪种情况，对应的结构体*表达式*中字段可以按任意顺序给出；得到的 `struct` 值总是具有相同的内存布局。

r[type.struct.field-visibility]
`struct` 的字段可以用[可见性修饰符][visibility modifiers]限定，以便在模块外访问结构体中的数据。

r[type.struct.tuple]
*元组结构体*类型与结构体类型类似，只是字段是匿名的。

r[type.struct.unit]
*类单元结构体*类型与结构体类型类似，只是它没有字段。由关联的[结构体表达式][struct expression]构造的那个值，是该类型唯一的居民。

[^structtype]: `struct` 类型类似于 C 中的 `struct` 类型、ML 家族的 *record* 类型，或 Lisp 家族的 *struct* 类型。

[`repr` attribute]: ../type-layout.md#representations
[struct expression]: ../expressions/struct-expr.md
[visibility modifiers]: ../visibility-and-privacy.md
