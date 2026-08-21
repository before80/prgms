+++
title = "01-命名空间"
date = 2026-08-18T08:45:00+08:00
weight = 96
type = "docs"
description = "命名空间 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/names/namespaces.html](https://doc.rust-lang.org/reference/names/namespaces.html)

r[names.namespaces]
# 命名空间

r[names.namespaces.intro]
*命名空间*是已声明[名称][names]的逻辑分组。名称根据其所指实体的种类被分隔到不同的命名空间中。命名空间允许一个命名空间中出现的名称与另一命名空间中的同名不冲突。

存在若干不同的命名空间，各自包含不同种类的实体。对名称的使用会根据上下文在不同命名空间中查找该名称的声明，如[名称解析][name resolution]一章所述。

r[names.namespaces.kinds]
以下是命名空间及其对应实体的列表：

* 类型命名空间
    * [模块声明][Module declarations]
    * [外部 crate 声明][External crate declarations]
    * [外部 crate prelude][External crate prelude]项
    * [结构体][Struct]、[联合体][union]、[枚举][enum]、枚举变体声明
    * [Trait 项声明][Trait item declarations]
    * [类型别名][Type aliases]
    * [关联类型声明][Associated type declarations]
    * 内建类型：[布尔][boolean]、[数值][numeric]、[`char`] 与 [`str`]
    * [泛型类型参数][Generic type parameters]
    * [`Self` 类型][`Self` type]
    * [工具属性模块][Tool attribute modules]
* 值命名空间
    * [函数声明][Function declarations]
    * [常量项声明][Constant item declarations]
    * [静态项声明][Static item declarations]
    * [结构体构造函数][Struct constructors]
    * [枚举变体构造函数][Enum variant constructors]
    * [`Self` 构造函数][`Self` constructors]
    * [泛型常量参数][Generic const parameters]
    * [关联常量声明][Associated const declarations]
    * [关联函数声明][Associated function declarations]
    * 局部绑定 —— [`let`]、[`if let`]、[`while let`]、[`for`]、[`match`] 臂、[函数参数][function parameters]、[闭包参数][closure parameters]
    * 被捕获的[闭包][closure]变量
* 宏命名空间
    * [`macro_rules` 声明][`macro_rules` declarations]
    * [内建属性][Built-in attributes]
    * [工具属性][Tool attributes]
    * [类函数过程宏][Function-like procedural macros]
    * [派生宏][Derive macros]
    * [派生宏助手][Derive macro helpers]
    * [属性宏][Attribute macros]
* 生命周期命名空间
    * [泛型生命周期参数][Generic lifetime parameters]
* 标签命名空间
    * [循环标签][Loop labels]
    * [块标签][Block labels]

不同命名空间中重叠名称可无歧义使用的示例：

```rust
// Foo 在类型命名空间中引入一个类型，在值命名空间中引入一个构造函数。
struct Foo(u32);

// `Foo` 宏声明在宏命名空间中。
macro_rules! Foo {
    () => {};
}

// `f` 参数类型中的 `Foo` 指类型命名空间中的 `Foo`。
// `'Foo` 在生命周期命名空间中引入一个新的生命周期。
fn example<'Foo>(f: Foo) {
    // `Foo` 指值命名空间中的 `Foo` 构造函数。
    let ctor = Foo;
    // `Foo` 指宏命名空间中的 `Foo` 宏。
    Foo!{}
    // `'Foo` 在标签命名空间中引入一个标签。
    'Foo: loop {
        // `'Foo` 指 `'Foo` 生命周期参数，而 `Foo`
        // 指类型命名空间。
        let x: &'Foo Foo;
        // `'Foo` 指标签。
        break 'Foo;
    }
}
```

r[names.namespaces.without]
## 没有命名空间的具名实体

下列实体具有显式名称，但这些名称不属于任何特定命名空间。

### 字段

r[names.namespaces.without.fields]
尽管结构体、枚举与联合体的字段是具名的，具名字段并不位于显式命名空间中。它们只能通过[字段表达式][field expression]访问，该表达式仅检查被访问的特定类型的字段名。

### use 声明

r[names.namespaces.without.use]
[use 声明][use declaration]具有导入到作用域中的具名别名，但 `use` 项本身并不属于特定命名空间。相反，它可以根据所导入项的种类，将别名引入多个命名空间。

r[names.namespaces.sub-namespaces]
## 子命名空间

r[names.namespaces.sub-namespaces.intro]
宏命名空间分为两个子命名空间：一个用于[bang 风格宏][bang-style macros]，一个用于[属性][attributes]。解析属性时，作用域中的任何 bang 风格宏都会被忽略。反之，解析 bang 风格宏时会忽略作用域中的属性宏。这可防止一种风格遮蔽另一种风格。

例如，[`cfg` 属性][`cfg` attribute]与 [`cfg` 宏][`cfg` macro]是宏命名空间中同名的两个不同实体，但它们仍可在各自的上下文中使用。

<!-- ignore: requires external crates -->
> **注意**
> 无论子命名空间如何，`use` 导入仍不能在模块或块中为同一名称创建重复绑定。
>
> ```rust
> #[macro_export]
> macro_rules! mymac {
>     () => {};
> }
>
> use myattr::mymac; // error[E0252]: the name `mymac` is defined multiple times.
> ```

[`cfg` attribute]: ../conditional-compilation.md#the-cfg-attribute
[`cfg` macro]: ../conditional-compilation.md#the-cfg-macro
[`char`]: ../types/char.md
[`for`]: ../expressions/loop-expr.md#iterator-loops
[`if let`]: ../expressions/if-expr.md#if-let-patterns
[`let`]: ../statements.md#let-statements
[`macro_rules` declarations]: ../macros-by-example.md
[`match`]: ../expressions/match-expr.md
[`Self` constructors]: ../paths.md#self-1
[`Self` type]: ../paths.md#self-1
[`str`]: ../types/str.md
[`use` import]: ../items/use-declarations.md
[`while let`]: ../expressions/loop-expr.md#while-let-patterns
[Associated const declarations]: ../items/associated-items.md#associated-constants
[Associated function declarations]: ../items/associated-items.md#associated-functions-and-methods
[Associated type declarations]: ../items/associated-items.md#associated-types
[Attribute macros]: ../procedural-macros.md#the-proc_macro_attribute-attribute
[attributes]: ../attributes.md
[bang-style macros]: ../macros.md
[Block labels]: expr.loop.block-labels
[boolean]: ../types/boolean.md
[Built-in attributes]: ../attributes.md#built-in-attributes-index
[closure parameters]: ../expressions/closure-expr.md
[closure]: ../expressions/closure-expr.md
[Constant item declarations]: ../items/constant-items.md
[Derive macro helpers]: ../procedural-macros.md#derive-macro-helper-attributes
[Derive macros]: macro.proc.derive
[entity]: ../glossary.md#entity
[Enum variant constructors]: ../items/enumerations.md
[enum]: ../items/enumerations.md
[External crate declarations]: ../items/extern-crates.md
[External crate prelude]: preludes.md#extern-prelude
[field expression]: ../expressions/field-expr.md
[Function declarations]: ../items/functions.md
[function parameters]: ../items/functions.md#function-parameters
[Function-like procedural macros]: ../procedural-macros.md#the-proc_macro-attribute
[Generic const parameters]: ../items/generics.md#const-generics
[Generic lifetime parameters]: ../items/generics.md
[Generic type parameters]: ../items/generics.md
[Loop labels]: ../expressions/loop-expr.md#loop-labels
[Module declarations]: ../items/modules.md
[name resolution]: name-resolution.md
[names]: ../names.md
[numeric]: ../types/numeric.md
[Static item declarations]: ../items/static-items.md
[Struct constructors]: ../items/structs.md
[Struct]: ../items/structs.md
[Tool attribute modules]: ../attributes.md#tool-attributes
[Tool attributes]: ../attributes.md#tool-attributes
[Trait item declarations]: ../items/traits.md
[Type aliases]: ../items/type-aliases.md
[union]: ../items/unions.md
[use declaration]: ../items/use-declarations.md
