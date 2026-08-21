+++
title = "05-类型别名"
date = 2026-08-18T08:45:00+08:00
weight = 22
type = "docs"
description = "类型别名 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/items/type-aliases.html](https://doc.rust-lang.org/reference/items/type-aliases.html)

r[items.type]
# 类型别名

r[items.type.syntax]
```grammar,items
TypeAlias ->
    `type` IDENTIFIER GenericParams? ( `:` Bounds? )?
        WhereClause?
        ( `=` Type WhereClause?)? `;`
```

r[items.type.intro]
*类型别名*在其所在模块或块的[类型命名空间][type namespace]中为已有[类型][type]定义一个新名称。类型别名用关键字 `type` 声明。每个值都有单一、具体的类型，但可以实现若干不同的 trait，并可能与若干不同的类型约束兼容。

例如，下列定义将类型 `Point` 作为类型 `(u8, u8)`（无符号 8 位整数对的类型）的同义词：

```rust
type Point = (u8, u8);
let p: Point = (41, 68);
```

r[items.type.constructor-alias]
指向元组结构体或单元结构体的类型别名不能用来限定该类型的构造器：

```rust
struct MyStruct(u32);

use MyStruct as UseAlias;
type TypeAlias = MyStruct;

let _ = UseAlias(5); // 可以
let _ = TypeAlias(5); // 不行
```

r[items.type.associated-type]
类型别名在不作为[关联类型][associated type]使用时，必须包含 [Type][grammar-Type]，且不得包含 [Bounds]。

r[items.type.associated-trait]
类型别名在 [trait] 中作为[关联类型][associated type]使用时，不得包含 [Type][grammar-Type] 说明，但可以包含 [Bounds]。

r[items.type.associated-impl]
类型别名在 [trait impl] 中作为[关联类型][associated type]使用时，必须包含 [Type][grammar-Type] 说明，且不得包含 [Bounds]。

r[items.type.deprecated]
[trait impl] 中类型别名等号之前的 where 子句（如 `type TypeAlias<T> where T: Foo = Bar<T>`）已弃用。更推荐等号之后的 where 子句（如 `type TypeAlias<T> = Bar<T> where T: Foo`）。

[associated type]: associated-items.md#associated-types
[trait impl]: implementations.md#trait-implementations
[trait]: traits.md
[type namespace]: ../names/namespaces.md
[type]: ../types.md
