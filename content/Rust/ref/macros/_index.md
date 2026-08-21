+++
title = "第3章 宏"
date = 2026-08-18T08:45:00+08:00
weight = 12
type = "docs"
description = "宏 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/macros.html](https://doc.rust-lang.org/reference/macros.html)

r[macro]
# 宏

r[macro.intro]
Rust 的功能与语法可以通过称为宏的自定义定义来扩展。它们被赋予名称，并通过一致的语法调用：`some_extension!(...)`。

定义新宏有两种方式：

* [示例宏][Macros by Example] 以更高层、声明式的方式定义新语法。
* [过程宏][Procedural macros] 使用对输入 token 进行操作的函数，定义函数式宏、自定义 derive 以及自定义属性。

r[macro.invocation]
## 宏调用

r[macro.invocation.syntax]
```grammar,macros
MacroInvocation ->
    SimplePath `!` DelimTokenTree

DelimTokenTree ->
      `(` TokenTree* `)`
    | `[` TokenTree* `]`
    | `{` TokenTree* `}`

TokenTree ->
    Token _except [delimiters][lex.token.delim]_ | DelimTokenTree

MacroInvocationSemi ->
      SimplePath `!` `(` TokenTree* `)` `;`
    | SimplePath `!` `[` TokenTree* `]` `;`
    | SimplePath `!` `{` TokenTree* `}`
```

r[macro.invocation.intro]
宏调用在编译时展开宏，并用宏的结果替换该调用。宏可在下列情形中被调用：

r[macro.invocation.expr]
* [表达式][Expressions] 与 [语句][statements]

r[macro.invocation.pattern]
* [模式][Patterns]

r[macro.invocation.type]
* [类型][Types]

r[macro.invocation.item]
* [项][Items]，包括 [关联项][associated items]

r[macro.invocation.nested]
* [`macro_rules`] 转写器

r[macro.invocation.extern]
* [外部块][External blocks]

r[macro.invocation.item-statement]
当用作项或语句时，使用 [MacroInvocationSemi] 形式：在不使用花括号时，末尾需要分号。在宏调用或 [`macro_rules`] 定义之前从不允许 [可见性限定符][Visibility qualifiers]。

```rust
// 用作表达式。
let x = vec![1,2,3];

// 用作语句。
println!("Hello!");

// 用在模式中。
macro_rules! pat {
    ($i:ident) => (Some($i))
}

if let pat!(x) = Some(1) {
    assert_eq!(x, 1);
}

// 用在类型中。
macro_rules! Tuple {
    { $A:ty, $B:ty } => { ($A, $B) };
}

type N2 = Tuple!(i32, i32);

// 用作项。
## use std::cell::RefCell;
thread_local!(static FOO: RefCell<u32> = RefCell::new(1));

// 用作关联项。
macro_rules! const_maker {
    ($t:ty, $v:tt) => { const CONST: $t = $v; };
}
trait T {
    const_maker!{i32, 7}
}

// 宏中的宏调用。
macro_rules! example {
    () => { println!("Macro call in a macro!") };
}
// 外层宏 `example` 被展开，然后内层宏 `println` 被展开。
example!();
```

r[macro.invocation.name-resolution]

宏调用可通过两种作用域解析：

- 文本作用域
  - [文本作用域 `macro_rules`](01-macros-by-example/#r-macro.decl.scope.textual)
- 基于路径的作用域
  - [基于路径的作用域 `macro_rules`](01-macros-by-example/#r-macro.decl.scope.path-based)
  - [过程宏][Procedural macros]

[External blocks]: items/external-blocks.md
[Macros by Example]: macros-by-example.md
[Procedural Macros]: procedural-macros.md
[`macro_rules`]: macros-by-example.md
[associated items]: items/associated-items.md
[delimiters]: tokens.md#delimiters
[expressions]: expressions.md
[items]: items.md
[patterns]: patterns.md
[statements]: statements.md
[types]: types.md
[visibility qualifiers]: visibility-and-privacy.md
