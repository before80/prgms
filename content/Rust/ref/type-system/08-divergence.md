+++
title = "08-发散"
date = 2026-08-18T08:45:00+08:00
weight = 91
type = "docs"
description = "发散 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/divergence.html](https://doc.rust-lang.org/reference/divergence.html)

r[divergence]
# 发散

r[divergence.intro]
*发散表达式* 是永远不会正常执行完毕的表达式。

```rust
fn diverges() -> ! {
    panic!("This function never returns!");
}

fn example() {
    let x: i32 = diverges(); // 这一行永远不会执行完毕。
    println!("This is never printed: {x}");
}
```

关于特定表达式的发散行为，参见以下规则：

- [expr.block.diverging] —— 块表达式。
- [expr.if.diverging] —— `if` 表达式。
- [expr.loop.block-labels.type] —— 带 `break` 的带标签块表达式。
- [expr.loop.break-value.diverging] —— 带 `break` 的 `loop` 表达式。
- [expr.loop.break.diverging] —— `break` 表达式。
- [expr.loop.continue.diverging] —— `continue` 表达式。
- [expr.loop.infinite.diverging] —— 无限 `loop` 表达式。
- [expr.match.diverging] —— `match` 表达式。
- [expr.match.empty] —— 空的 `match` 表达式。
- [expr.return.diverging] —— `return` 表达式。
- [type.never.constraint] —— 返回 `!` 的函数调用。

> **注意**
> [`panic!`] 宏以及相关的产生 panic 的宏（如 [`unreachable!`]）也具有类型 [`!`]，并且是发散的。

r[divergence.never]
任何类型为 [`!`] 的表达式都是发散表达式。然而，发散表达式并不限于类型 [`!`]；其他类型的表达式也可能发散（例如，`Some(loop {})` 的类型为 `Option<!>`）。

> **注意**
> 尽管 `!` 被视为无居住值类型，但一个类型无居住值并不足以使其发散。
>
> ```rust
> enum Empty {}
> fn make_never() -> ! {loop{}}
> fn make_empty() -> Empty {loop{}}
>
> fn diverging() -> ! {
>     // 这具有类型 `!`。
>     // 因此，整个函数被视为发散。
>     make_never();
>     // 正确：函数体的类型为 `!`，与返回类型匹配。
> }
> fn not_diverging() -> ! {
>     // 此类型无居住值。
>     // 然而，整个函数并不被视为发散。
>     make_empty();
>     // 错误：函数体的类型为 `()`，但期望类型为 `!`。
> }
> ```

> **注意**
> 发散可以传播到外围的块。参见 [expr.block.diverging]。

r[divergence.fallback]
## 回退

若一个待推断的类型只与发散表达式进行了合一，则该类型将被推断为 [`!`]。

> [!EXAMPLE]
> ```rust
> fn foo() -> i32 { 22 }
> match foo() {
>     // 错误：未满足 trait 约束 `!: Default`。
>     4 => Default::default(),
>     _ => return,
> };
> ```

> [!EDITION-2024]
> 在 2024 edition 之前，该类型会被推断为 `()`。

> **注意**
> 重要的是，类型合一可能以 *结构化* 的方式发生，因此回退的 `!` 可能是更大类型的一部分。下面的代码可以编译：
>
> ```rust
> fn foo() -> i32 { 22 }
> // 这具有类型 `Option<!>`，而不是 `!`
> match foo() {
>     4 => Default::default(),
>     _ => Some(return),
> };
> ```

<!-- TODO: 最后这一点很可能应移到更一般的「类型推断」章节，讨论泛化与合一。 -->

[`!`]: type.never
