+++
title = "01-布尔类型"
date = 2026-08-18T08:45:00+08:00
weight = 66
type = "docs"
description = "布尔类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types/boolean.html](https://doc.rust-lang.org/reference/types/boolean.html)

r[type.bool]
# 布尔类型

```rust
let b: bool = true;
```

r[type.bool.intro]
*布尔类型*或 *bool* 是一种基本数据类型，只能取两个值之一，分别称为 *true* 和 *false*。

r[type.bool.literal]
该类型的值可以用[字面量表达式][literal expression]创建，关键字 `true` 和 `false` 对应同名的值。

r[type.bool.namespace]
该类型属于[语言 prelude][language prelude]，其[名称][name]为 `bool`。

r[type.bool.layout]
布尔类型对象的[大小和对齐][size and alignment]均为 1。

r[type.bool.repr]
`false` 的位模式为 `0x00`，`true` 的位模式为 `0x01`。布尔类型对象具有任何其他位模式都是[未定义行为][undefined behavior]。

r[type.bool.use]
布尔类型是多种[表达式][expressions]中许多操作数的类型：

r[type.bool.use-in-condition]
* [if 表达式][if expressions]和 [while 表达式][while expressions]中的条件操作数

r[type.bool.use-in-lazy-operator]
* [惰性布尔运算符表达式][lazy]中的操作数

> **注意**
> 布尔类型的行为与[枚举类型][enumerated type]类似，但并不是枚举类型。实践中，这主要意味着构造函数并不关联到该类型（例如没有 `bool::true`）。

r[type.bool.traits]
与所有基本类型一样，布尔类型[实现][p-impl]了 [trait][p-traits] [`Clone`][p-clone]、[`Copy`][p-copy]、[`Sized`][p-sized]、[`Send`][p-send] 和 [`Sync`][p-sync]。

> **注意**
> 库层面的操作见[标准库文档](bool)。

r[type.bool.expr]
## 布尔值上的运算

当某些运算符表达式的操作数是布尔类型时，它们按[布尔逻辑][boolean logic]的规则求值。

r[type.bool.expr.not]
### 逻辑非

| `b` | [`!b`][op-not] |
|- | - |
| `true` | `false` |
| `false` | `true` |

r[type.bool.expr.or]
### 逻辑或

| `a` | `b` | [`a \| b`][op-or] |
|- | - | - |
| `true` | `true` | `true` |
| `true` | `false` | `true` |
| `false` | `true` | `true` |
| `false` | `false` | `false` |

r[type.bool.expr.and]
### 逻辑与

| `a` | `b` | [`a & b`][op-and] |
|- | - | - |
| `true` | `true` | `true` |
| `true` | `false` | `false` |
| `false` | `true` | `false` |
| `false` | `false` | `false` |

r[type.bool.expr.xor]
### 逻辑异或

| `a` | `b` | [`a ^ b`][op-xor] |
|- | - | - |
| `true` | `true` | `false` |
| `true` | `false` | `true` |
| `false` | `true` | `true` |
| `false` | `false` | `false` |

r[type.bool.expr.cmp]
### 比较

r[type.bool.expr.cmp.eq]
| `a` | `b` | [`a == b`][op-compare] |
|- | - | - |
| `true` | `true` | `true` |
| `true` | `false` | `false` |
| `false` | `true` | `false` |
| `false` | `false` | `true` |

r[type.bool.expr.cmp.greater]
| `a` | `b` | [`a > b`][op-compare] |
|- | - | - |
| `true` | `true` | `false` |
| `true` | `false` | `true` |
| `false` | `true` | `false` |
| `false` | `false` | `false` |

r[type.bool.expr.cmp.not-eq]
* `a != b` 等价于 `!(a == b)`

r[type.bool.expr.cmp.greater-eq]
* `a >= b` 等价于 `a == b | a > b`

r[type.bool.expr.cmp.less]
* `a < b` 等价于 `!(a >= b)`

r[type.bool.expr.cmp.less-eq]
* `a <= b` 等价于 `a == b | a < b`

r[type.bool.validity]
## 位有效性

`bool` 的那一个字节保证已初始化（换句话说，`transmute::<bool, u8>(...)` 总是健全的——但由于某些位模式不是合法 `bool`，反过来并不总是健全）。

[boolean logic]: https://en.wikipedia.org/wiki/Boolean_algebra
[enumerated type]: enum.md
[expressions]: ../expressions.md
[if expressions]: ../expressions/if-expr.md#if-expressions
[language prelude]: ../names/preludes.md#language-prelude
[lazy]: ../expressions/operator-expr.md#lazy-boolean-operators
[literal expression]: ../expressions/literal-expr.md
[name]: ../names.md
[op-and]: ../expressions/operator-expr.md#arithmetic-and-logical-binary-operators
[op-compare]: ../expressions/operator-expr.md#comparison-operators
[op-not]: ../expressions/operator-expr.md#negation-operators
[op-or]: ../expressions/operator-expr.md#arithmetic-and-logical-binary-operators
[op-xor]: ../expressions/operator-expr.md#arithmetic-and-logical-binary-operators
[p-clone]: ../special-types-and-traits.md#clone
[p-copy]: ../special-types-and-traits.md#copy
[p-impl]: ../items/implementations.md
[p-send]: ../special-types-and-traits.md#send
[p-sized]: ../special-types-and-traits.md#sized
[p-sync]: ../special-types-and-traits.md#sync
[p-traits]: ../items/traits.md
[size and alignment]: ../type-layout.md#size-and-alignment
[undefined behavior]: ../behavior-considered-undefined.md
[while expressions]: ../expressions/loop-expr.md#predicate-loops
