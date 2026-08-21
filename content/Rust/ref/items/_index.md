+++
title = "第6章 项"
date = 2026-08-18T08:45:00+08:00
weight = 17
type = "docs"
description = "项 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/items.html](https://doc.rust-lang.org/reference/items.html)

r[items]
# 项

r[items.syntax]
```grammar,items
Item ->
    OuterAttribute* ( VisItem | MacroItem )

VisItem ->
    Visibility?
    (
        Module
      | ExternCrate
      | UseDeclaration
      | Function
      | TypeAlias
      | Struct
      | Enumeration
      | Union
      | ConstantItem
      | StaticItem
      | Trait
      | Implementation
      | ExternBlock
    )

MacroItem ->
      MacroInvocationSemi
    | MacroRulesDefinition
```

r[items.intro]
*项*（item）是 crate 的组成部分。项通过嵌套的[模块]集合组织在 crate 中。每个 crate 都有一个最外层的匿名模块；crate 中的所有其他项都在该 crate 的模块树中拥有[路径]。

r[items.static-def]
项完全在编译期确定，执行期间通常保持不变，并且可以驻留在只读内存中。

r[items.kinds]
项有若干种类：

* [模块][modules]
* [`extern crate` 声明][`extern crate` declarations]
* [`use` 声明][`use` declarations]
* [函数定义][function definitions]
* [类型别名定义][type alias definitions]
* [结构体定义][struct definitions]
* [枚举定义][enumeration definitions]
* [联合体定义][union definitions]
* [常量项][constant items]
* [静态项][static items]
* [trait 定义][trait definitions]
* [实现][implementations]
* [`extern` 块][`extern` blocks]

r[items.locations]
项可以在 [crate 根][root of the crate]、[模块][modules] 或[块表达式][block expression]中声明。

r[items.associated-locations]
一部分项称为[关联项][associated items]，可以在 [trait][traits] 和[实现][implementations]中声明。

r[items.extern-locations]
一部分项称为外部项，可以在 [`extern` 块][`extern` blocks]中声明。

r[items.decl-order]
项可以按任意顺序定义，但 [`macro_rules`] 例外，它有自己的作用域规则。

r[items.name-resolution]
项名称的[名称解析][Name resolution]允许项在模块或块中被引用之前或之后定义。

关于项的作用域规则，参见[项作用域][item scopes]。

[`extern crate` declarations]: items/extern-crates.md
[`extern` blocks]: items/external-blocks.md
[`macro_rules`]: macros-by-example.md
[`use` declarations]: items/use-declarations.md
[associated items]: items/associated-items.md
[block expression]: expressions/block-expr.md
[constant items]: items/constant-items.md
[enumeration definitions]: items/enumerations.md
[function definitions]: items/functions.md
[implementations]: items/implementations.md
[item scopes]: names/scopes.md#item-scopes
[modules]: items/modules.md
[name resolution]: names/name-resolution.md
[paths]: paths.md
[root of the crate]: crates-and-source-files.md
[statement]: statements.md
[static items]: items/static-items.md
[struct definitions]: items/structs.md
[trait definitions]: items/traits.md
[traits]: items/traits.md
[type alias definitions]: items/type-aliases.md
[union definitions]: items/unions.md
