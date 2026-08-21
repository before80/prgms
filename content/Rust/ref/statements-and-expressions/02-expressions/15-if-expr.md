+++
title = "15-if 表达式"
date = 2026-08-18T08:45:00+08:00
weight = 58
type = "docs"
description = "if 表达式 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/expressions/if-expr.html](https://doc.rust-lang.org/reference/expressions/if-expr.html)

r[expr.if]
# if 表达式

r[expr.if.syntax]
```grammar,expressions
IfExpression ->
    `if` Conditions BlockExpressionNoInnerAttributes
    (`else` ( BlockExpressionNoInnerAttributes | IfExpression ) )?

Conditions ->
      Expression _except [StructExpression]_
    | LetChain

LetChain -> LetChainCondition ( `&&` LetChainCondition )*

LetChainCondition ->
      Expression _except [ExcludedConditions]_
    | OuterAttribute* `let` Pattern `=` Scrutinee _except [ExcludedConditions]_

@root ExcludedConditions ->
      StructExpression
    | LazyBooleanExpression
    | RangeExpr
    | RangeFromExpr
    | RangeInclusiveExpr
    | AssignmentExpression
    | CompoundAssignmentExpression
```
<!-- TODO: The struct exception above needs clarification, see https://github.com/rust-lang/reference/issues/1808
     The chain grammar could use some work, see https://github.com/rust-lang/reference/issues/1811
-->

r[expr.if.intro]
`if` 表达式的语法是：由 `&&` 分隔的一个或多个条件操作数，后跟一个 then 块、任意数量的 `else if` 条件和块，以及一个可选的结尾 `else` 块。

r[expr.if.condition]
条件操作数必须是具有[布尔类型][boolean type]的[表达式][Expression]，或是条件式 `let` 匹配。

r[expr.if.condition-true]
若所有条件操作数都求值为 `true`，且所有 `let` 模式都成功匹配其[被检视表达式][scrutinee]，则执行 then 块，并跳过任何后续的 `else if` 或 `else` 块。

r[expr.if.else-if]
若任一条件操作数求值为 `false`，或任一 `let` 模式未能匹配其被检视表达式，则跳过 then 块，并求值任何后续的 `else if` 条件。

r[expr.if.else]
若所有 `if` 和 `else if` 条件都求值为 `false`，则执行任何 `else` 块。

r[expr.if.result]
`if` 表达式求值为所执行块的值；若没有块被求值，则为 `()`。

r[expr.if.type]
`if` 表达式在所有情况下必须具有相同的类型。

```rust
## let x = 3;
if x == 4 {
    println!("x is four");
} else if x == 3 {
    println!("x is three");
} else {
    println!("x is something else");
}

// `if` 可以用作表达式。
let y = if 12 * 15 > 150 {
    "Bigger"
} else {
    "Smaller"
};
assert_eq!(y, "Bigger");
```

r[expr.if.diverging]
若条件表达式发散，或所有分支都发散，则 `if` 表达式[发散][diverges]。

```rust
fn diverging_condition() -> ! {
    // 发散，因为条件表达式发散
    if loop {} {
        ()
    } else {
        ()
    };
    // 上面的分号很重要：尽管该 `if` 表达式发散，
    // 其类型仍为 `()`。当省略最终的函数体表达式时，
    // 函数体的类型被推断为 !，因为函数体发散。
    // 若没有分号，该 `if` 会成为尾表达式，类型为 `()`，
    // 从而无法匹配返回类型 `!`。
}

fn diverging_arms() -> ! {
    // 发散，因为所有分支都发散
    if true {
        loop {}
    } else {
        loop {}
    }
}
```

r[expr.if.let]
## `if let` 模式

r[expr.if.let.intro]
`if` 条件中的 `let` 模式允许在模式匹配成功时把新变量绑定到作用域中。

以下示例演示了使用 `let` 模式的绑定：

```rust
let dish = ("Ham", "Eggs");

// 该函数体会被跳过，因为模式被反驳。
if let ("Bacon", b) = dish {
    println!("Bacon is served with {}", b);
} else {
    // 改为求值这个块。
    println!("No bacon will be served");
}

// 该函数体会执行。
if let ("Ham", b) = dish {
    println!("Ham is served with {}", b);
}

if let _ = 5 {
    println!("Irrefutable patterns are always true");
}
```

r[expr.if.let.or-pattern]
可以用 `|` 运算符指定多个模式。其语义与 [`match` 表达式][`match` expressions]中的 `|` 相同：

```rust
enum E {
    X(u8),
    Y(u8),
    Z(u8),
}
let v = E::Y(12);
if let E::X(n) | E::Y(n) = v {
    assert_eq!(n, 12);
}
```

r[expr.if.chains]
## 条件链

r[expr.if.chains.intro]
多个条件操作数可以用 `&&` 分隔。

r[expr.if.chains.order]
与 `&&` [LazyBooleanExpression] 类似，各操作数从左到右求值，直到某个操作数求值为 `false` 或某个 `let` 匹配失败，此后的操作数不再求值。

r[expr.if.chains.bindings]
每个模式的绑定都会进入作用域，供下一个条件操作数和 then 块使用。

以下示例演示了串联多个表达式、混合 `let` 绑定与布尔表达式，并且后续表达式可以引用先前表达式中的模式绑定：

```rust
fn single() {
    let outer_opt = Some(Some(1i32));

    if let Some(inner_opt) = outer_opt
        && let Some(number) = inner_opt
        && number == 1
    {
        println!("Peek a boo");
    }
}
```

以上写法等价于下面不使用条件链的形式：

```rust
fn nested() {
    let outer_opt = Some(Some(1i32));

    if let Some(inner_opt) = outer_opt {
        if let Some(number) = inner_opt {
            if number == 1 {
                println!("Peek a boo");
            }
        }
    }
}
```

r[expr.if.chains.or]
若任一条件操作数是 `let` 模式，则任何条件操作数都不能是 `||` [惰性布尔运算符表达式][expr.bool-logic]，以免与 `let` 被检视表达式产生歧义和优先级问题。

> [!EXAMPLE]
> 若需要 `||` 表达式，可以使用圆括号。例如：
>
> ```rust
> # let foo = Some(123);
> # let condition1 = true;
> # let condition2 = false;
> if let Some(x) = foo
>     // 此处需要圆括号。
>     && (condition1 || condition2)
> {}
> ```

r[expr.if.edition2024]
> [!EDITION-2024]
> 在 2024 edition 之前不支持 let 链。也就是说，`if` 表达式中不允许使用 [LetChain] 语法。

[`match` expressions]: match-expr.md
[boolean type]: ../types/boolean.md
[diverges]: divergence
[scrutinee]: ../glossary.md#scrutinee
