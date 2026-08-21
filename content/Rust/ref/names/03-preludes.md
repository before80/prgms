+++
title = "03-Prelude"
date = 2026-08-18T08:45:00+08:00
weight = 98
type = "docs"
description = "Prelude — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/names/preludes.html](https://doc.rust-lang.org/reference/names/preludes.html)

r[names.preludes]
# Prelude

r[names.preludes.intro]
*prelude* 是自动带入 crate 中每个模块作用域的一组名称集合。

这些 prelude 名称不是模块本身的一部分：它们在[名称解析][name resolution]期间被隐式查询。例如，即便像 [`Box`] 这样的名称在每个模块中都处于作用域内，也不能用 `self::Box` 引用它，因为它不是当前模块的成员。

r[names.preludes.kinds]
存在若干不同的 prelude：

- [标准库 prelude][Standard library prelude]
- [外部 prelude][Extern prelude]
- [语言 prelude][Language prelude]
- [`macro_use` prelude]
- [工具 prelude][Tool prelude]

r[names.preludes.std]
## 标准库 prelude

r[names.preludes.std.intro]
每个 crate 都有一个标准库 prelude，由单个标准库模块中的名称组成。

r[names.preludes.std.module]
所用模块取决于 crate 的 edition，以及是否对 crate 应用了 [`no_std` 属性][`no_std` attribute]：

Edition | 未应用 `no_std`        | 已应用 `no_std`
--------| --------------------------- | ----------------------------
2015    | [`std::prelude::rust_2015`] | [`core::prelude::rust_2015`]
2018    | [`std::prelude::rust_2018`] | [`core::prelude::rust_2018`]
2021    | [`std::prelude::rust_2021`] | [`core::prelude::rust_2021`]
2024    | [`std::prelude::rust_2024`] | [`core::prelude::rust_2024`]

> **注意**
> [`std::prelude::rust_2015`] 与 [`std::prelude::rust_2018`] 的内容与 [`std::prelude::v1`] 相同。
>
> [`core::prelude::rust_2015`] 与 [`core::prelude::rust_2018`] 的内容与 [`core::prelude::v1`] 相同。

> **注意**
> 当因[标准库 prelude][standard library prelude]而将 [`core::panic!`] 或 [`std::panic!`] 之一带入作用域，且用户编写的 [glob 导入][glob import]将另一个带入作用域时，`rustc` 目前允许使用 `panic!`，即便它是有歧义的。用户编写的 glob 导入优先以消除此歧义。
>
> 详情参见 [names.resolution.expansion.imports.ambiguity.panic-hack]。

r[names.preludes.extern]
## 外部 prelude

r[names.preludes.extern.intro]
在根模块中用 [`extern crate`] 导入的、或提供给编译器的（例如对 `rustc` 使用 `--extern` 标志）外部 crate，会被加入*外部 prelude*。若使用别名导入，例如 `extern crate orig_name as new_name`，则符号 `new_name` 会被加入 prelude。

r[names.preludes.extern.core]
[`core`] crate 总是被加入外部 prelude。

r[names.preludes.extern.std]
只要 crate 根未指定 [`no_std` 属性][`no_std` attribute]，就会加入 [`std`] crate。

r[names.preludes.extern.edition2018]
> [!EDITION-2018]
> 在 2015 edition 中，外部 prelude 中的 crate 不能通过 [use 声明][use declarations]引用，因此通常的标准做法是包含 `extern crate` 声明以将它们带入作用域。
>
> 从 2018 edition 开始，[use 声明][use declarations]可以引用外部 prelude 中的 crate，因此使用 `extern crate` 被认为不符合惯用法。

> **注意**
> 随 `rustc` 一并提供的其他 crate，例如 [`alloc`] 与 [`test`](mod@test)，在使用 Cargo 时不会通过 `--extern` 标志自动包含。即使在 2018 edition 中，也必须用 `extern crate` 声明将它们带入作用域。
>
> ```rust
> extern crate alloc;
> use alloc::rc::Rc;
> ```
>
> Cargo 仅为过程宏 crate 将 `proc_macro` 带入外部 prelude。

<!--
See https://github.com/rust-lang/rust/issues/57288 for more about the alloc/test limitation.
-->

<!-- template:attributes -->
r[names.preludes.extern.no_std]
### `no_std` 属性

r[names.preludes.extern.no_std.intro]
*`no_std` [属性][attributes]* 使 [`std`] crate 不会被自动链接，并使[标准库 prelude][standard library prelude]改用 `core` prelude。

> [!EXAMPLE]
> <!-- ignore: test infrastructure can't handle no_std -->
> ```rust
> #![no_std]
> ```

> **注意**
> 当 crate 面向不支持标准库的平台，或有意不使用标准库的能力时，使用 `no_std` 很有用。这些能力主要是动态内存分配（例如 `Box` 与 `Vec`）以及文件与网络能力（例如 `std::fs` 与 `std::io`）。

> **警告**
> 使用 `no_std` 并不会阻止标准库被链接。在 crate 或其依赖之一中编写 `extern crate std` 仍然有效；这将使编译器将 `std` crate 链接进程序。

r[names.preludes.extern.no_std.syntax]
`no_std` 属性使用 [MetaWord] 语法。

r[names.preludes.extern.no_std.allowed-positions]
`no_std` 属性只能应用于 crate 根。

r[names.preludes.extern.no_std.duplicates]
`no_std` 属性可以在一个形式上使用任意次数。

> **注意**
> `rustc` 会对第一次之后的任何使用发出 lint。

r[names.preludes.extern.no_std.module]
`no_std` 属性会使[标准库 prelude][standard library prelude]使用 `core` prelude，而不是 `std` prelude。

r[names.preludes.extern.no_std.edition2018]
> [!EDITION-2018]
> 在 2018 edition 之前，默认会将 `std` 注入到 crate 根。若指定了 `no_std`，则改为注入 `core`。从 2018 edition 开始，无论是否指定 `no_std`，都不会将二者注入到 crate 根。

r[names.preludes.lang]
## 语言 prelude

r[names.preludes.lang.intro]
语言 prelude 包括语言内建的类型与属性名称。语言 prelude 始终处于作用域中。

r[names.preludes.lang.entities]
它包括下列内容：

* [类型命名空间][Type namespace]
    * [布尔类型][Boolean type] —— `bool`
    * [`char`]
    * [`str`]
    * [整数类型][Integer types] —— `i8`、`i16`、`i32`、`i64`、`i128`、`u8`、`u16`、`u32`、`u64`、`u128`
    * [机器相关整数类型][Machine-dependent integer types] —— `usize` 与 `isize`
    * [浮点类型][floating-point types] —— `f32` 与 `f64`
* [宏命名空间][Macro namespace]
    * [内建属性][Built-in attributes]
    * [内建派生宏][attributes.derive.built-in]

r[names.preludes.macro_use]
## `macro_use` prelude

r[names.preludes.macro_use.intro]
`macro_use` prelude 包括通过应用于 [`extern crate`] 的 [`macro_use` 属性][`macro_use` attribute]从外部 crate 导入的宏。

r[names.preludes.tool]
## 工具 prelude

r[names.preludes.tool.intro]
工具 prelude 在[类型命名空间][type namespace]中包含外部工具的工具名称。更多细节参见[工具属性][tool attributes]一节。

<!-- template:attributes -->
r[names.preludes.no_implicit_prelude]
## `no_implicit_prelude` 属性

r[names.preludes.no_implicit_prelude.intro]
*`no_implicit_prelude` [属性][attribute]* 用于防止隐式 prelude 被带入作用域。

> [!EXAMPLE]
> ```rust
> // 该属性可应用于 crate 根以影响
> // 所有模块。
> #![no_implicit_prelude]
>
> // 或者可应用于模块，仅影响该模块
> // 及其后代。
> #[no_implicit_prelude]
> mod example {
>     // ...
> }
> ```

r[names.preludes.no_implicit_prelude.syntax]
`no_implicit_prelude` 属性使用 [MetaWord] 语法。

r[names.preludes.no_implicit_prelude.allowed-positions]
`no_implicit_prelude` 属性只能应用于 crate 或模块。

> **注意**
> `rustc` 会忽略其他位置上的使用，但会对其发出 lint。将来这可能变为错误。

r[names.preludes.no_implicit_prelude.duplicates]
`no_implicit_prelude` 属性可以在一个形式上使用任意次数。

> **注意**
> `rustc` 会对第一次之后的任何使用发出 lint。

r[names.preludes.no_implicit_prelude.excluded-preludes]
`no_implicit_prelude` 属性会阻止将[标准库 prelude][standard library prelude]、[外部 prelude][extern prelude]、[`macro_use` prelude] 与[工具 prelude][tool prelude]带入该模块及其后代的作用域。

r[names.preludes.no_implicit_prelude.implicitly-imported-macros]
> **注意**
> 尽管有 `#![no_implicit_prelude]`，`rustc` 目前仍会将某些宏隐式带入作用域。这些宏是：
>
> - [`assert!`]
> - [`cfg!`]
> - [`cfg_select!`]
> - [`column!`]
> - [`compile_error!`]
> - [`concat!`]
> - [`concat_bytes!`]
> - [`env!`]
> - [`file!`]
> - [`format_args!`]
> - [`include!`]
> - [`include_bytes!`]
> - [`include_str!`]
> - [`line!`]
> - [`module_path!`]
> - [`option_env!`]
> - [`panic!`]
> - [`stringify!`]
> - [`unreachable!`]
>
> 例如，这样是有效的：
>
> ```rust
> #![no_implicit_prelude]
> fn main() { assert!(true); }
> ```
>
> 不要依赖此行为；它将来可能被移除。使用 `#![no_implicit_prelude]` 时，始终显式将所需项带入作用域。
>
> 详情参见 [Rust PR #62086](https://github.com/rust-lang/rust/pull/62086) 与 [Rust PR #139493](https://github.com/rust-lang/rust/pull/139493)。

r[names.preludes.no_implicit_prelude.lang]
`no_implicit_prelude` 属性不影响[语言 prelude][language prelude]。

r[names.preludes.no_implicit_prelude.edition2018]
> [!EDITION-2018]
> 在 2015 edition 中，`no_implicit_prelude` 属性不影响 [`macro_use` prelude]，标准库导出的所有宏仍包含在 `macro_use` prelude 中。从 2018 edition 开始，该属性会移除 `macro_use` prelude。

[`char`]: ../types/char.md
[`extern crate`]: ../items/extern-crates.md
[`macro_use` attribute]: ../macros-by-example.md#the-macro_use-attribute
[`macro_use` prelude]: #macro_use-prelude
[`no_std` attribute]: #the-no_std-attribute
[`str`]: ../types/str.md
[attribute]: ../attributes.md
[Boolean type]: ../types/boolean.md
[Built-in attributes]: ../attributes.md#built-in-attributes-index
[extern prelude]: #extern-prelude
[floating-point types]: ../types/numeric.md#floating-point-types
[glob import]: items.use.glob
[Integer types]: ../types/numeric.md#integer-types
[Language prelude]: #language-prelude
[Machine-dependent integer types]: ../types/numeric.md#machine-dependent-integer-types
[Macro namespace]: namespaces.md
[name resolution]: name-resolution.md
[standard library prelude]: names.preludes.std
[tool attributes]: ../attributes.md#tool-attributes
[Tool prelude]: #tool-prelude
[Type namespace]: namespaces.md
[use declarations]: ../items/use-declarations.md
