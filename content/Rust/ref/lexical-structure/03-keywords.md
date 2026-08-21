+++
title = "03-关键字"
date = 2026-08-18T08:45:00+08:00
weight = 7
type = "docs"
description = "关键字 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/keywords.html](https://doc.rust-lang.org/reference/keywords.html)

r[lex.keywords]
# 关键字

Rust 将关键字分为三类：

* [严格](#严格关键字)
* [保留](#保留关键字)
* [弱](#弱关键字)

r[lex.keywords.strict]
## 严格关键字

r[lex.keywords.strict.intro]
这些关键字只能在其正确的上下文中使用。它们不能用作下列名称：

* [项][Items]
* [变量][Variables] 与函数参数
* 字段与 [变体][variants]
* [类型参数][Type parameters]
* 生命周期参数或 [循环标签][loop labels]
* [宏][Macros] 或 [属性][attributes]
* [宏占位符][Macro placeholders]
* [Crate][Crates]

r[lex.keywords.strict.list]
下列关键字在所有 edition 中都存在：

- `_`
- `as`
- `async`
- `await`
- `break`
- `const`
- `continue`
- `crate`
- `dyn`
- `else`
- `enum`
- `extern`
- `false`
- `fn`
- `for`
- `if`
- `impl`
- `in`
- `let`
- `loop`
- `match`
- `mod`
- `move`
- `mut`
- `pub`
- `ref`
- `return`
- `self`
- `Self`
- `static`
- `struct`
- `super`
- `trait`
- `true`
- `type`
- `unsafe`
- `use`
- `where`
- `while`

r[lex.keywords.strict.edition2018]
> [!EDITION-2018]
> 下列关键字是在 2018 edition 中加入的：
>
> - `async`
> - `await`
> - `dyn`

r[lex.keywords.reserved]
## 保留关键字

r[lex.keywords.reserved.intro]
这些关键字尚未使用，但为将来使用而保留。它们与严格关键字有相同的限制。这样做的理由是：通过禁止当前程序使用这些关键字，使当前程序与未来版本的 Rust 向前兼容。

r[lex.keywords.reserved.list]
- `abstract`
- `become`
- `box`
- `do`
- `final`
- `gen`
- `macro`
- `override`
- `priv`
- `try`
- `typeof`
- `unsized`
- `virtual`
- `yield`

r[lex.keywords.reserved.edition2018]
> [!EDITION-2018]
> `try` 关键字在 2018 edition 中被加入为保留关键字。

r[lex.keywords.reserved.edition2024]
> [!EDITION-2024]
> `gen` 关键字在 2024 edition 中被加入为保留关键字。

r[lex.keywords.weak]
## 弱关键字

r[lex.keywords.weak.intro]
这些关键字仅在特定上下文中具有特殊含义。例如，可以声明名为 `union` 的变量或方法。

- `'static`
- `macro_rules`
- `raw`
- `safe`
- `union`

r[lex.keywords.weak.macro_rules]
* `macro_rules` 用于创建自定义 [宏][macros]。

r[lex.keywords.weak.union]
* `union` 用于声明 [联合体][union]，且仅在联合体声明中使用时才是关键字。

r[lex.keywords.weak.lifetime-static]
* `'static` 用于静态生命周期，不能用作 [泛型生命周期参数][generic lifetime parameter] 或 [循环标签][loop label]

  ```compile_fail
  // error[E0262]: 无效的生命周期参数名：`'static`
  fn invalid_lifetime_parameter<'static>(s: &'static str) -> &'static str { s }
  ```

r[lex.keywords.weak.safe]
* `safe` 用于函数和静态项，在 [外部块][external blocks] 中具有含义。

r[lex.keywords.weak.raw]
* `raw` 用于 [原始借用运算符][raw borrow operators]，且仅在匹配原始借用运算符形式（如 `&raw const expr` 或 `&raw mut expr`）时才是关键字。

r[lex.keywords.weak.dyn.edition2018]
> [!EDITION-2018]
> 在 2015 edition 中，当 [`dyn`] 用在类型位置，且其后跟随不以 `::` 或 `<` 开头的路径、生命周期、问号、`for` 关键字或开括号时，它是关键字。
>
> 从 2018 edition 开始，`dyn` 已被提升为严格关键字。

[items]: items.md
[Variables]: variables.md
[Type parameters]: types/parameters.md
[loop labels]: expressions/loop-expr.md#loop-labels
[Macros]: macros.md
[attributes]: attributes.md
[Macro placeholders]: macros-by-example.md
[Crates]: crates-and-source-files.md
[union]: items/unions.md
[variants]: items/enumerations.md
[`dyn`]: types/trait-object.md
[loop label]: expressions/loop-expr.md#loop-labels
[generic lifetime parameter]: items/generics.md
[external blocks]: items/external-blocks.md
[raw borrow operators]: expressions/operator-expr.md#raw-borrow-operators
