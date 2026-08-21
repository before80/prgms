+++
title = "12-闭包表达式"
date = 2026-08-18T08:45:00+08:00
weight = 55
type = "docs"
description = "闭包表达式 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/expressions/closure-expr.html](https://doc.rust-lang.org/reference/expressions/closure-expr.html)

r[expr.closure]
# 闭包表达式

r[expr.closure.syntax]
```grammar,expressions
ClosureExpression ->
    `async`?[^cl-async-edition]
    `move`?
    ( `||` | `|` ClosureParameters? `|` )
    (Expression | `->` TypeNoBounds BlockExpression)

ClosureParameters -> ClosureParam (`,` ClosureParam)* `,`?

ClosureParam -> OuterAttribute* PatternNoTopAlt ( `:` Type )?
```

[^cl-async-edition]: 2015 edition 中不允许使用 `async` 限定符。

r[expr.closure.intro]
*闭包表达式*也称 lambda 表达式或 lambda，它定义一种[闭包类型][closure type]并求值为该类型的值。闭包表达式的语法是：可选的 `async` 关键字、可选的 `move` 关键字，然后是由管道符（`|`）括起、以逗号分隔的[模式][patterns]列表（称为*闭包参数*，每个参数后可选择跟 `:` 和类型），然后是可选的 `->` 和类型（称为*返回类型*），最后是一个表达式（称为*闭包体操作数*）。

r[expr.closure.param-type]
每个模式后可选的类型是该模式的类型注解。

r[expr.closure.explicit-type-body]
若存在返回类型，则闭包体必须是[块][block]。

r[expr.closure.parameter-restriction]
闭包表达式表示一个函数，把参数列表映射到参数之后的那个表达式。与 [`let` 绑定][`let` binding]一样，闭包参数是不可反驳[模式][patterns]，类型注解可选；若未给出，将从上下文推断。

r[expr.closure.unique-type]
每个闭包表达式都有唯一的匿名类型。

r[expr.closure.captures]
重要的是，闭包表达式会_捕获其环境_，而普通的[函数定义][function definitions]不会。

r[expr.closure.capture-inference]
没有 `move` 关键字时，闭包表达式会[推断它如何从环境中捕获每个变量](../../type-system/01-types/13-closure/#capture-modes)，优先以共享引用捕获，相当于借用闭包体中提到的所有外部变量。

r[expr.closure.capture-mut-ref]
若有需要，编译器会转而推断应采用可变引用，或应从环境中移动或复制这些值（取决于其类型）。

r[expr.closure.capture-move]
可以在闭包前加上 `move` 关键字，强制通过复制或移动值来捕获环境。这常用于确保闭包的生命周期为 `'static`。

r[expr.closure.trait-impl]
## 闭包的 trait 实现

闭包类型实现哪些 trait 取决于变量如何被捕获、被捕获变量的类型，以及是否存在 `async`。关于闭包何时以及如何实现 `Fn`、`FnMut` 和 `FnOnce`，见[调用 trait 与强制转换][call traits and coercions]一章。若每个被捕获变量的类型也都实现了相应 trait，则闭包类型实现 [`Send`] 和 [`Sync`]。

r[expr.closure.async]
## 异步闭包

r[expr.closure.async.intro]
带 `async` 关键字的闭包表示它们是异步的，其方式与[异步函数][items.fn.async]类似。

r[expr.closure.async.future]
调用异步闭包并不会执行任何工作，而是求值为一个实现了 [`Future`]、对应于闭包体计算的值。

```rust
async fn takes_async_callback(f: impl AsyncFn(u64)) {
    f(0).await;
    f(1).await;
}

async fn example() {
    takes_async_callback(async |i| {
        core::future::ready(i).await;
        println!("done with {i}.");
    }).await;
}
```

r[expr.closure.async.edition2018]
> [!EDITION-2018]
> 异步闭包从 Rust 2018 起才可用。

## 示例

本例中，我们定义函数 `ten_times`，它接受一个高阶函数参数，然后我们以闭包表达式作为参数调用它，接着再传入一个从环境中移出值的闭包表达式。

```rust
fn ten_times<F>(f: F) where F: Fn(i32) {
    for index in 0..10 {
        f(index);
    }
}

ten_times(|j| println!("hello, {}", j));
// 带类型注解
ten_times(|j: i32| -> () { println!("hello, {}", j) });

let word = "konnichiwa".to_owned();
ten_times(move |j| println!("{}, {}", word, j));
```

## 闭包参数上的属性

r[expr.closure.param-attributes]
闭包参数上的属性遵循与[普通函数参数][regular function parameters]相同的规则和限制。

[`let` binding]: ../statements.md#let-statements
[`Send`]: ../special-types-and-traits.md#send
[`Sync`]: ../special-types-and-traits.md#sync
[block]: block-expr.md
[call traits and coercions]: ../types/closure.md#call-traits-and-coercions
[closure type]: ../types/closure.md
[function definitions]: ../items/functions.md
[patterns]: ../patterns.md
[regular function parameters]: ../items/functions.md#attributes-on-function-parameters
