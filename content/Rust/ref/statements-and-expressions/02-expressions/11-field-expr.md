+++
title = "11-字段访问表达式"
date = 2026-08-18T08:45:00+08:00
weight = 54
type = "docs"
description = "字段访问表达式 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/expressions/field-expr.html](https://doc.rust-lang.org/reference/expressions/field-expr.html)

r[expr.field]
# 字段访问表达式

r[expr.field.syntax]
```grammar,expressions
FieldExpression -> Expression `.` IDENTIFIER
```

r[expr.field.intro]
*字段表达式*是一种[位置表达式][place expression]，求值为[结构体][struct]或[联合体][union]某个字段所在的位置。

r[expr.field.mut]
当操作数[可变][mutable]时，字段表达式也是可变的。

r[expr.field.form]
字段表达式的语法是：一个表达式（称为*容器操作数*），然后是 `.`，最后是一个[标识符][identifier]。

r[expr.field.not-method-call]
字段表达式后面不能跟由圆括号括起、以逗号分隔的表达式列表，因为那会被解析为[方法调用表达式][method call expression]。也就是说，它们不能作为[调用表达式][call expression]的函数操作数。

> **注意**
> 将字段表达式包在[圆括号表达式][parenthesized expression]中，即可在调用表达式中使用它。
>
> ```rust
> # struct HoldsCallable<F: Fn()> { callable: F }
> let holds_callable = HoldsCallable { callable: || () };
>
> // 非法：会被解析为调用名为 "callable" 的方法
> // holds_callable.callable();
>
> // 合法
> (holds_callable.callable)();
> ```

示例：

<!-- ignore: needs lots of support code -->
```rust
mystruct.myfield;
foo().x;
(Struct {a: 10, b: 20}).a;
(mystruct.function_field)() // 包含字段表达式的调用表达式
```

r[expr.field.autoref-deref]
## 自动解引用

若容器操作数的类型实现了 [`Deref`] 或 [`DerefMut`][`Deref`]（取决于操作数是否[可变][mutable]），则会*自动解引用*足够多次以使字段访问成为可能。该过程也简称 *autoderef*。

r[expr.field.borrow]
## 借用

在借用时，结构体的各个字段或对结构体的引用被当作彼此独立的实体。若该结构体未实现 [`Drop`] 且存储在局部变量中，这也适用于从各个字段中移出。若自动解引用是通过 [`Box`] 以外的用户定义类型完成的，则上述规则不适用。

```rust
struct A { f1: String, f2: String, f3: String }
let mut x: A;
## x = A {
##     f1: "f1".to_string(),
##     f2: "f2".to_string(),
##     f3: "f3".to_string()
## };
let a: &mut String = &mut x.f1; // x.f1 被可变借用
let b: &String = &x.f2;         // x.f2 被不可变借用
let c: &String = &x.f2;         // 可以再次借用
let d: String = x.f3;           // 从 x.f3 移出
```

[`Box`]: ../special-types-and-traits.md#boxt
[`Deref`]: ../special-types-and-traits.md#deref-and-derefmut
[`drop`]: ../special-types-and-traits.md#drop
[identifier]: ../identifiers.md
[call expression]: call-expr.md
[method call expression]: method-call-expr.md
[mutable]: ../expressions.md#mutability
[parenthesized expression]: grouped-expr.md
[place expression]: ../expressions.md#place-expressions-and-value-expressions
[struct]: ../items/structs.md
[union]: ../items/unions.md
