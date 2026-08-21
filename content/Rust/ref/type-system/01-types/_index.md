+++
title = "01-类型"
date = 2026-08-18T08:45:00+08:00
weight = 65
type = "docs"
description = "类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types.html](https://doc.rust-lang.org/reference/types.html)

r[type]
# 类型

r[type.intro]
Rust 程序中的每个变量、项和值都有一个类型。*值*的*类型*定义了保存该值的内存如何被解释，以及可以对它执行哪些操作。

r[type.builtin]
内置类型与语言紧密集成，其方式并非平凡，无法用用户定义类型来完全模拟。

r[type.user-defined]
用户定义类型的能力有限。

r[type.kinds]
类型列表如下：

* 基本类型：
    * [布尔类型][Boolean] --- `bool`
    * [数值类型][Numeric] --- 整数和浮点数
    * [`char`]
    * [`str`]
    * [Never] --- `!` --- 没有值的类型
* 序列类型：
    * [元组][Tuple]
    * [数组][Array]
    * [切片][Slice]
* 用户定义类型：
    * [结构体][Struct]
    * [枚举][Enum]
    * [联合体][Union]
* 函数类型：
    * [函数][Functions]
    * [闭包][Closures]
* 指针类型：
    * [引用][References]
    * [裸指针][Raw pointers]
    * [函数指针][Function pointers]
* Trait 类型：
    * [Trait 对象][Trait objects]
    * [Impl trait]

r[type.name]
## 类型表达式

r[type.name.syntax]
```grammar,types
Type ->
      TypeNoBounds
    | ImplTraitType
    | TraitObjectType

TypeNoBounds ->
      ParenthesizedType
    | ImplTraitTypeOneBound
    | TraitObjectTypeOneBound
    | TypePath
    | TupleType
    | NeverType
    | RawPointerType
    | ReferenceType
    | ArrayType
    | SliceType
    | InferredType
    | QualifiedPathInType
    | BareFunctionType
    | MacroInvocation
```

r[type.name.intro]
上文 [Type] 文法规则所定义的*类型表达式*是引用类型的语法。它可以引用：

r[type.name.sequence]
* 序列类型（[元组][tuple]、[数组][array]、[切片][slice]）。

r[type.name.path]
* [类型路径][Type paths]，可以引用：
    * 基本类型（[布尔类型][boolean]、[数值类型][numeric]、[`char`]、[`str`]）。
    * 指向[项][item]的路径（[结构体][struct]、[枚举][enum]、[联合体][union]、[类型别名][type alias]、[trait]）。
    * [`Self` 路径][`Self` path]，其中 `Self` 是正在实现的类型。
    * 泛型[类型参数][type parameters]。

r[type.name.pointer]
* 指针类型（[引用][reference]、[裸指针][raw pointer]、[函数指针][function pointer]）。

r[type.name.inference]
* [推断类型][inferred type]，请求编译器确定类型。

r[type.name.grouped]
* 用于消歧的[括号][Parentheses]。

r[type.name.trait]
* Trait 类型：[Trait 对象][Trait objects]和 [impl trait]。

r[type.name.never]
* [Never][never] 类型。

r[type.name.macro-expansion]
* 展开为类型表达式的[宏][Macros]。

r[type.name.parenthesized]
### 括号类型

r[type.name.parenthesized.syntax]
```grammar,types
ParenthesizedType -> `(` Type `)`
```

r[type.name.parenthesized.intro]
在某些情况下，类型的组合可能产生歧义。在类型外加括号可避免歧义。例如，[引用类型][reference type]中用于[类型边界][type boundaries]的 `+` 运算符，其边界作用范围并不清楚，因此必须使用括号。需要这种消歧的文法规则使用 [TypeNoBounds] 规则，而不是 [Type][grammar-Type]。

```rust
## use std::any::Any;
type T<'a> = &'a (dyn Any + Send);
```

r[type.recursive]
## 递归类型

r[type.recursive.intro]
指名类型——[结构体][structs]、[枚举][enumerations]和[联合体][unions]——可以是递归的。也就是说，每个 `enum` 变体或 `struct`/`union` 字段都可以直接或间接地引用包围它的 `enum` 或 `struct` 类型本身。

r[type.recursive.constraint]
这种递归有如下限制：

* 递归类型必须在递归中包含指名类型（不能仅仅是[类型别名][type aliases]，或其他结构类型，如[数组][arrays]或[元组][tuples]）。因此不允许 `type Rec = &'static [Rec]`。
* 递归类型的大小必须是有限的；换句话说，该类型的递归字段必须是[指针类型][pointer types]。

*递归*类型及其使用示例：

```rust
enum List<T> {
    Nil,
    Cons(T, Box<List<T>>)
}

let a: List<i32> = List::Cons(7, Box::new(List::Cons(13, Box::new(List::Nil))));
```

[`char`]: types/char.md
[`str`]: types/str.md
[Array]: types/array.md
[Boolean]: types/boolean.md
[Closures]: types/closure.md
[Enum]: types/enum.md
[Function pointers]: types/function-pointer.md
[Functions]: types/function-item.md
[Impl trait]: types/impl-trait.md
[Macros]: macros.md
[Numeric]: types/numeric.md
[Parentheses]: #parenthesized-types
[Raw pointers]: types/pointer.md#raw-pointers-const-and-mut
[References]: types/pointer.md#shared-references-
[Slice]: types/slice.md
[Struct]: types/struct.md
[Trait objects]: types/trait-object.md
[Tuple]: types/tuple.md
[Type paths]: paths.md#paths-in-types
[Union]: types/union.md
[`Self` path]: paths.md#self-1
[arrays]: types/array.md
[enumerations]: types/enum.md
[function pointer]: types/function-pointer.md
[inferred type]: types/inferred.md
[item]: items.md
[never]: types/never.md
[pointer types]: types/pointer.md
[raw pointer]: types/pointer.md#raw-pointers-const-and-mut
[reference type]: types/pointer.md#shared-references-
[reference]: types/pointer.md#shared-references-
[structs]: types/struct.md
[trait]: types/trait-object.md
[tuples]: types/tuple.md
[type alias]: items/type-aliases.md
[type aliases]: items/type-aliases.md
[type boundaries]: trait-bounds.md
[type parameters]: types/parameters.md
[unions]: types/union.md
