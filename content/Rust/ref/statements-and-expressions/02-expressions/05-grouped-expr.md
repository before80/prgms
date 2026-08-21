+++
title = "05-分组表达式"
date = 2026-08-18T08:45:00+08:00
weight = 48
type = "docs"
description = "分组表达式 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/expressions/grouped-expr.html](https://doc.rust-lang.org/reference/expressions/grouped-expr.html)

r[expr.paren]
# 分组表达式

r[expr.paren.syntax]
```grammar,expressions
GroupedExpression -> `(` Expression `)`
```

r[expr.paren.intro]
*圆括号表达式*包装单个表达式，其求值结果就是该表达式。圆括号表达式的语法是 `(`，然后是一个表达式（称为*被括操作数*），最后是 `)`。

r[expr.paren.evaluation]
圆括号表达式求值为被括操作数的值。

r[expr.paren.place-or-value]
若被括操作数是[位置表达式][place]，则圆括号表达式是位置表达式；若被括操作数是值表达式，则圆括号表达式是值表达式。

r[expr.paren.override-precedence]
圆括号可用于显式修改表达式中子表达式的优先级顺序。

圆括号表达式的示例：

```rust
let x: i32 = 2 + 3 * 4; // 未加括号
let y: i32 = (2 + 3) * 4; // 已加括号
assert_eq!(x, 14);
assert_eq!(y, 20);
```

必须使用圆括号的一个例子是：调用作为结构体成员的函数指针时：

```rust
## struct A {
##    f: fn() -> &'static str
## }
## impl A {
##    fn f(&self) -> &'static str {
##        "The method f"
##    }
## }
## let a = A{f: || "The field f"};
#
assert_eq!( a.f (), "The method f");
assert_eq!((a.f)(), "The field f");
```

[place]: ../expressions.md#place-expressions-and-value-expressions
