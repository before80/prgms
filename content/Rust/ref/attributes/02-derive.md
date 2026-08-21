+++
title = "02-Derive"
date = 2026-08-18T08:45:00+08:00
weight = 35
type = "docs"
description = "Derive — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/attributes/derive.html](https://doc.rust-lang.org/reference/attributes/derive.html)

<!-- template:attributes -->
r[attributes.derive]
# Derive

r[attributes.derive.intro]
*`derive` [属性][attributes]*会调用一个或多个 [derive 宏][derive macros]，从而为数据结构自动生成新的[项][items]。你可以通过[过程宏][procedural macros]创建 `derive` 宏。

> [!EXAMPLE]
> [`PartialEq`][macro@PartialEq] derive 宏会为 `Foo<T> where T: PartialEq` 生成 [`PartialEq`] 的[实现][implementation]。[`Clone`][macro@Clone] derive 宏对 [`Clone`] 同理。
>
> ```rust
> #[derive(PartialEq, Clone)]
> struct Foo<T> {
>     a: i32,
>     b: T,
> }
> ```
>
> 生成的 `impl` 项等价于：
>
> ```rust
> # struct Foo<T> { a: i32, b: T }
> impl<T: PartialEq> PartialEq for Foo<T> {
>     fn eq(&self, other: &Foo<T>) -> bool {
>         self.a == other.a && self.b == other.b
>     }
> }
>
> impl<T: Clone> Clone for Foo<T> {
>     fn clone(&self) -> Self {
>         Foo { a: self.a.clone(), b: self.b.clone() }
>     }
> }
> ```

r[attributes.derive.syntax]
`derive` 属性使用 [MetaListPaths] 语法，指定要调用的 [derive 宏][derive macros]路径列表。

r[attributes.derive.allowed-positions]
`derive` 属性只能应用于[结构体][items.struct]、[枚举][items.enum]和[联合体][items.union]。

r[attributes.derive.duplicates]
`derive` 属性可在同一项上使用任意次数。所有属性中列出的 derive 宏都会被调用。

r[attributes.derive.stdlib]
`derive` 属性在标准库中导出为：

- [`core::derive`]
- [`std::derive`]
- [`core::prelude::v1::derive`]
- [`std::prelude::v1::derive`]

r[attributes.derive.built-in]
内置 derive 定义在[语言 prelude][names.preludes.lang] 中。内置 derive 列表如下：

- [`Clone`]
- [`Copy`]
- [`Debug`]
- [`Default`]
- [`Eq`]
- [`Hash`]
- [`Ord`]
- [`PartialEq`]
- [`PartialOrd`]

r[attributes.derive.built-in-automatically_derived]
内置 derive 会在其生成的实现上包含 [`automatically_derived` 属性][attributes.derive.automatically_derived]。

r[attributes.derive.behavior]
在宏展开期间，对于 derive 列表中的每个元素，对应的 derive 宏会展开为零个或多个[项][items]。

<!-- template:attributes -->
r[attributes.derive.automatically_derived]
## `automatically_derived` 属性

r[attributes.derive.automatically_derived.intro]
*`automatically_derived` [属性][attributes]*用于标注某个[实现][implementation]，表明它是由 [derive 宏][derive macro]自动创建的。它没有直接效果，但可供工具与诊断 lint 用来检测这些自动生成的实现。

> [!EXAMPLE]
> 在 `struct Example` 上使用 [`#[derive(Clone)]`][macro@Clone] 时，[derive 宏][derive macro]可能生成：
>
> ```rust
> # struct Example;
> #[automatically_derived]
> impl ::core::clone::Clone for Example {
>     #[inline]
>     fn clone(&self) -> Self {
>         Example
>     }
> }
> ```

r[attributes.derive.automatically_derived.syntax]
`automatically_derived` 属性使用 [MetaWord] 语法。

r[attributes.derive.automatically_derived.allowed-positions]
`automatically_derived` 属性只能应用于[实现][implementation]。

> **注意**
> `rustc` 会忽略其他位置上的使用，但会对其发出 lint。将来这可能变成错误。

r[attributes.derive.automatically_derived.duplicates]
在同一实现上多次使用 `automatically_derived` 与使用一次效果相同。

> **注意**
> `rustc` 会对第一次之后的使用发出 lint。

r[attributes.derive.automatically_derived.behavior]
`automatically_derived` 属性没有行为。

[items]: ../items.md
[derive macro]: macro.proc.derive
[derive macros]: macro.proc.derive
[implementation]: ../items/implementations.md
[items]: ../items.md
[procedural macros]: macro.proc.derive
