+++
title = "14-区间表达式"
date = 2026-08-18T08:45:00+08:00
weight = 57
type = "docs"
description = "区间表达式 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/expressions/range-expr.html](https://doc.rust-lang.org/reference/expressions/range-expr.html)

r[expr.range]
# 区间表达式

r[expr.range.syntax]
```grammar,expressions
RangeExpression ->
      RangeExpr
    | RangeFromExpr
    | RangeToExpr
    | RangeFullExpr
    | RangeInclusiveExpr
    | RangeToInclusiveExpr

RangeExpr -> Expression `..` Expression

RangeFromExpr -> Expression `..`

RangeToExpr -> `..` Expression

RangeFullExpr -> `..`

RangeInclusiveExpr -> Expression `..=` Expression

RangeToInclusiveExpr -> `..=` Expression
```

r[expr.range.behavior]
`..` 和 `..=` 运算符会根据下表构造 `std::ops::Range`（或 `core::ops::Range`）的某个变体对象：

| 产生式                 | 语法          | 类型                         | 区间                  |
|------------------------|---------------|------------------------------|-----------------------|
| [RangeExpr]            | start`..`end  | [std::ops::Range]            | start &le; x &lt; end |
| [RangeFromExpr]        | start`..`     | [std::ops::RangeFrom]        | start &le; x          |
| [RangeToExpr]          | `..`end       | [std::ops::RangeTo]          |            x &lt; end |
| [RangeFullExpr]        | `..`          | [std::ops::RangeFull]        |            -          |
| [RangeInclusiveExpr]   | start`..=`end | [std::ops::RangeInclusive]   | start &le; x &le; end |
| [RangeToInclusiveExpr] | `..=`end      | [std::ops::RangeToInclusive] |            x &le; end |

示例：

```rust
1..2;   // std::ops::Range
3..;    // std::ops::RangeFrom
..4;    // std::ops::RangeTo
..;     // std::ops::RangeFull
5..=6;  // std::ops::RangeInclusive
..=7;   // std::ops::RangeToInclusive
```

r[expr.range.equivalence]
下列表达式等价。

```rust
let x = std::ops::Range {start: 0, end: 10};
let y = 0..10;

assert_eq!(x, y);
```

r[expr.range.for]
区间可用于 `for` 循环：

```rust
for i in 1..11 {
    println!("{}", i);
}
```
