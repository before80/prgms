+++
title = "02-动态大小类型"
date = 2026-08-18T08:45:00+08:00
weight = 85
type = "docs"
description = "动态大小类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/dynamically-sized-types.html](https://doc.rust-lang.org/reference/dynamically-sized-types.html)

r[dynamic-sized]
# 动态大小类型

r[dynamic-sized.intro]
大多数类型具有在编译时已知的固定大小，并实现 trait [`Sized`][sized]。大小仅在运行时才知道的类型称为 _动态大小类型_（_DST_），非正式地也称为不定大小类型。[切片][Slices]、[trait 对象][trait objects]和 [str] 都是 <abbr title="dynamically sized types">DST</abbr> 的例子。

r[dynamic-sized.restriction]
此类类型只能在某些情况下使用：

r[dynamic-sized.pointer-types]
* 指向 <abbr title="dynamically sized types">DST</abbr> 的[指针类型][Pointer types]是有大小的，但其大小是指向有大小类型的指针的两倍，因为它们还存储 *元数据*：
    * 指向切片的指针存储元素个数；指向 `str` 的指针存储以字节计的长度。
    * 指向 trait 对象的指针存储指向 vtable 的指针。
    * 指向带有[不定大小尾部][unsized tail]的结构体或元组的指针，存储与指向该尾部的指针相同的元数据。

r[dynamic-sized.question-sized]
* <abbr title="dynamically sized types">DST</abbr> 可以作为类型实参提供给具有特殊 `?Sized` 约束的泛型类型参数。当相应的关联类型声明具有 `?Sized` 约束时，它们也可以用于关联类型定义。默认情况下，任何类型参数或关联类型都具有 `Sized` 约束，除非使用 `?Sized` 将其放宽。

r[dynamic-sized.trait-impl]
* Trait 可以为 <abbr title="dynamically sized
  types">DST</abbr> 实现。与泛型类型参数不同，在 trait 定义中，`Self: ?Sized` 是默认情况。

r[dynamic-sized.struct-field]
* 结构体可以将 <abbr title="dynamically sized type">DST</abbr> 作为最后一个字段；这会使该结构体自身也成为 <abbr title="dynamically sized type">DST</abbr>。

> **注意**
> [变量][Variables]、函数参数、[const] 项和 [static] 项必须是 `Sized` 的。

r[dynamic-sized.tail]
一个类型的 *不定大小尾部* 是指向该类型的指针的[元数据][metadata]所描述的动态大小组成部分。[切片][slice]（`[T]`）和 [`str`] 各自是自己的不定大小尾部，由长度描述；[trait 对象][trait object]（`dyn Trait`）是自己的不定大小尾部，由指向 vtable 的指针描述。当结构体（见 [dynamic-sized.struct-field]）或元组的最后一个字段不定大小时，其不定大小尾部就是该字段的不定大小尾部。有大小的类型没有不定大小尾部。

[metadata]: dynamic-sized.pointer-types
[sized]: special-types-and-traits.md#sized
[unsized tail]: dynamic-sized.tail
[Slices]: types/slice.md
[slice]: types/slice.md
[str]: types/str.md
[`str`]: types/str.md
[trait objects]: types/trait-object.md
[trait object]: types/trait-object.md
[Pointer types]: types/pointer.md
[Variables]: variables.md
[const]: items/constant-items.md
[static]: items/static-items.md
