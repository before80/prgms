+++
title = "01-语句"
date = 2026-08-18T08:45:00+08:00
weight = 42
type = "docs"
description = "语句 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/statements.html](https://doc.rust-lang.org/reference/statements.html)

r[statement]
# 语句

r[statement.syntax]
```grammar,statements
Statement ->
      `;`
    | Item
    | LetStatement
    | ExpressionStatement
    | OuterAttribute* MacroInvocationSemi
```

r[statement.intro]
*语句*是[块][block]的组成部分，而块又是外层[表达式][expression]或[函数][function]的组成部分。

r[statement.kind]
Rust 有两类语句：[声明语句](#declaration-statements)与[表达式语句](#expression-statements)。

r[statement.decl]
## 声明语句

*声明语句*会向包围它的语句块中引入一个或多个*名字*。所声明的名字可以表示新变量或新的[项][item]。

两类声明语句分别是项声明与 `let` 语句。

r[statement.item]
### 项声明

r[statement.item.intro]
*项声明语句*的语法形式与[模块][module]内的[项声明][item]相同。

r[statement.item.scope]
在语句块内声明项会将其[作用域][scope]限制为包含该语句的块。该项不会获得[规范路径][canonical path]，其可能声明的任何子项也不会。

r[statement.item.associated-scope]
例外是：[实现][implementations]所定义的关联项，只要该项以及（如适用）trait 可访问，就仍可在外层作用域中访问。除此之外，其含义与在模块内声明该项完全相同。

r[statement.item.outer-generics]
不会隐式捕获外围函数的泛型参数、参数以及局部变量。例如，`inner` 不能访问 `outer_var`。

```rust
fn outer() {
  let outer_var = true;

  fn inner() { /* outer_var 在此处不在作用域内 */ }

  inner();
}
```

r[statement.let]
### `let` 语句

r[statement.let.syntax]
```grammar,statements
LetStatement ->
    OuterAttribute* `let` PatternNoTopAlt ( `:` Type )?
    (
          `=` Expression
        | `=` Expression _except [LazyBooleanExpression] or end with a `}`_
              `else` BlockExpressionNoInnerAttributes
    )? `;`
```

r[statement.let.intro]
*`let` 语句*通过[模式][pattern]引入一组新的[变量][variables]。模式之后可选地跟类型注解，然后要么结束，要么跟初始化表达式以及可选的 `else` 块。

r[statement.let.inference]
未给出类型注解时，编译器会推断类型；若没有足够的类型信息以确定推断，则会报错。

r[statement.let.scope]
变量声明所引入的任何变量，从声明点起直到包围块作用域结束都可见，除非被另一变量声明遮蔽。

r[statement.let.constraint]
若不存在 `else` 块，模式必须是不可失败的（irrefutable）。若存在 `else` 块，模式可以是可失败的（refutable）。

r[statement.let.behavior]
若模式不匹配（这要求它是可失败的），则执行 `else` 块。`else` 块必须始终发散（求值为[从不类型][never type]）。

```rust
let (mut v, w) = (vec![1, 2, 3], 42); // 绑定可以是 mut 或 const
let Some(t) = v.pop() else { // 可失败模式需要 else 块
    panic!(); // else 块必须发散
};
let [u, v] = [v[0], v[1]] else { // 此模式不可失败，因此编译器
                                 // 会发出 lint，因为 else 块是多余的。
    panic!();
};
```

r[statement.expr]
## 表达式语句

r[statement.expr.syntax]
```grammar,statements
ExpressionStatement ->
      ExpressionWithoutBlock `;`
    | ExpressionWithBlock `;`?
```

r[statement.expr.intro]
*表达式语句*会求值一个[表达式][expression]并忽略其结果。通常，表达式语句的目的是触发求值其表达式所带来的副作用。

r[statement.expr.restriction-semicolon]
仅由[块表达式][block]或控制流表达式构成的表达式，若用在允许语句的上下文中，可以省略尾随分号。这可能导致它被解析为独立语句还是另一表达式的一部分之间产生歧义；在此情况下，它会被解析为语句。

r[statement.expr.constraint-block]
当 [ExpressionWithBlock] 表达式用作语句时，其类型必须是单元类型。

```rust
## let mut v = vec![1, 2, 3];
v.pop();          // 忽略 pop 返回的元素
if v.is_empty() {
    v.push(5);
} else {
    v.remove(0);
}                 // 可以省略分号。
[1];              // 独立的表达式语句，而非索引表达式。
```

省略尾随分号时，结果的类型必须是 `()`。

```rust
// 错误：该块的类型是 i32，而非 ()
// 错误：由于默认返回类型，期望 `()`
// if true {
//   1
// }

// 正确：该块的类型是 i32
if true {
  1
} else {
  2
};
```

r[statement.attribute]
## 语句上的属性

语句接受[外部属性][outer attributes]。对语句有意义的属性是 [`cfg`]，以及[lint 检查属性][the lint check attributes]。

[block]: expressions/block-expr.md
[expression]: expressions.md
[function]: items/functions.md
[item]: items.md
[module]: items/modules.md
[never type]: types/never.md
[canonical path]: paths.md#canonical-paths
[implementations]: items/implementations.md
[variables]: variables.md
[outer attributes]: attributes.md
[`cfg`]: conditional-compilation.md
[the lint check attributes]: attributes/diagnostics.md#lint-check-attributes
[pattern]: patterns.md
[scope]: names/scopes.md
