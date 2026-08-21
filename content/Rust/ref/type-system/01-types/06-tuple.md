+++
title = "06-元组类型"
date = 2026-08-18T08:45:00+08:00
weight = 71
type = "docs"
description = "元组类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types/tuple.html](https://doc.rust-lang.org/reference/types/tuple.html)

r[type.tuple]
# 元组类型

r[type.tuple.syntax]
```grammar,types
TupleType ->
      `(` `)`
    | `(` ( Type `,` )+ Type? `)`
```

r[type.tuple.intro]
*元组类型*是一族结构类型[^1]，用于表示其他类型的异构列表。

元组类型的语法是括号括起、逗号分隔的类型列表。

r[type.tuple.restriction]
一元元组必须在其元素类型后加逗号，以便与[括号类型][parenthesized type]区分。

r[type.tuple.field-number]
元组类型的字段数等于类型列表的长度。该字段数决定了元组的*元数*。有 `n` 个字段的元组称为 *n 元元组*。例如，有 2 个字段的元组是二元元组。

r[type.tuple.field-name]
元组字段使用与其在类型列表中位置相匹配的递增数字名称。第一个字段是 `0`。第二个字段是 `1`。依此类推。每个字段的类型就是元组类型列表中相同位置的类型。

r[type.tuple.unit]
出于方便和历史原因，没有字段的元组类型（`()`）常称为*单元*或*单元类型*。它唯一的值也称为*单元*或*单元值*。

一些元组类型的例子：

* `()`（单元）
* `(i32,)`（一元元组）
* `(f64, f64)`
* `(String, i32)`
* `(i32, String)`（与上一个示例不同类型）
* `(i32, f64, Vec<String>, Option<bool>)`

r[type.tuple.constructor]
该类型的值用[元组表达式][tuple expression]构造。此外，各种表达式在没有其他有意义的求值结果时会产生单元值。

r[type.tuple.access]
元组字段可以通过[元组索引表达式][tuple index expression]或[模式匹配][pattern matching]访问。

[^1]: 若内部类型等价，则结构类型总是等价。元组的指名版本见[元组结构体][tuple structs]。

[parenthesized type]: ../types.md#parenthesized-types
[pattern matching]: ../patterns.md#tuple-patterns
[tuple expression]: ../expressions/tuple-expr.md#tuple-expressions
[tuple index expression]: ../expressions/tuple-expr.md#tuple-indexing-expressions
[tuple structs]: ./struct.md
