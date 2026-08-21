+++
title = "02-语法索引"
date = 2026-08-18T08:45:00+08:00
weight = 117
type = "docs"
description = "语法索引 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/syntax-index.html](https://doc.rust-lang.org/reference/syntax-index.html)

# 语法索引

本附录提供 token 与常见形式的索引，并链接到这些元素的定义处。

## 关键字

| 关键字       | 用途 |
|---------------|-----|
| `_`           | [通配符模式][wildcard pattern]、[推断的常量][inferred const]、[推断的类型][inferred type]、[占位生命周期][placeholder lifetime]、[常量项][constant items]、[extern crate]、[use 声明][use declarations]、[解构赋值][destructuring assignment] |
| `abstract`    | [保留关键字][reserved keyword] |
| `as`          | [extern crate][items.extern-crate.as]、[use 声明][items.use.forms.as]、[类型强制转换表达式][type cast expressions]、[限定路径][qualified paths] |
| `async`       | [async 函数][async functions]、[async 块][async blocks]、[async 闭包][async closures] |
| `await`       | [await 表达式][await expressions] |
| `become`      | [保留关键字][reserved keyword] |
| `box`         | [保留关键字][reserved keyword] |
| `break`       | [break 表达式][break expressions] |
| `const`       | [常量函数][const functions]、[常量项][const items]、[常量泛型][const generics]、[const 块][const blocks]、[裸借用运算符][raw borrow operator]、[裸指针类型][raw pointer type]、[常量汇编操作数][const assembly operands] |
| `continue`    | [continue 表达式][continue expressions] |
| `crate`       | [extern crate]、[可见性][visibility]、[路径][paths] |
| `do`          | [保留关键字][reserved keyword] |
| `dyn`         | [trait 对象][trait objects] |
| `else`        | [let 语句][let statements]、[if 表达式][if expressions] |
| `enum`        | [枚举][enumerations] |
| `extern`      | [extern crate]、[extern 函数限定符][extern function qualifier]、[外部块][external blocks]、[extern 函数指针类型][extern function pointer types] |
| `false`       | [布尔类型][boolean type]、[布尔表达式][boolean expressions]、[配置谓词][configuration predicates] |
| `final`       | [保留关键字][reserved keyword] |
| `fn`          | [函数][functions]、[函数指针类型][function pointer types] |
| `for`         | [trait 实现][trait implementations]、[迭代器循环][iterator loops]、[高阶 trait 约束][higher-ranked trait bounds] |
| `gen`         | [保留关键字][reserved keyword] |
| `if`          | [if 表达式][if expressions]、[match 守卫][match guards] |
| `impl`        | [固有 impl][inherent impls]、[trait impl][trait impls]、[impl trait 类型][impl trait types]、[匿名类型参数][anonymous type parameters] |
| `in`          | [可见性][visibility]、[迭代器循环][iterator loops]、[汇编操作数][assembly operands] |
| `let`         | [let 语句][let statements]、[`if let` 模式][`if let` patterns] |
| `loop`        | [无限循环][infinite loops] |
| `macro_rules` | [示例宏][macros by example] |
| `macro`       | [保留关键字][reserved keyword] |
| `match`       | [match 表达式][match expressions] |
| `mod`         | [模块][modules] |
| `move`        | [闭包表达式][closure expressions]、[async 块][async blocks] |
| `mut`         | [借用表达式][borrow expressions]、[标识符模式][identifier patterns]、[引用模式][reference patterns]、[结构体模式][struct patterns]、[引用类型][reference types]、[裸指针类型][raw pointer types]、[self 参数][self parameters]、[静态项][static items] |
| `override`    | [保留关键字][reserved keyword] |
| `priv`        | [保留关键字][reserved keyword] |
| `pub`         | [可见性][visibility] |
| `raw`         | [借用表达式][borrow expressions]、[裸汇编][raw assembly] |
| `ref`         | [标识符模式][identifier patterns]、[结构体模式][struct patterns] |
| `return`      | [return 表达式][return expressions] |
| `safe`        | [外部块函数][external block functions]、[外部块静态项][external block statics] |
| `self`        | [extern crate][items.extern-crate.self]、[self 参数][self parameters]、[可见性][visibility]、[`self` 路径][`self` paths] |
| `Self`        | [`Self` 类型路径][`Self` type paths]、[use 约束][use bounds] |
| `static`      | [静态项][static items]、[`'static` 生命周期][`'static` lifetimes] |
| `struct`      | [结构体][structs] |
| `super`       | [super 路径][super paths]、[可见性][visibility] |
| `trait`       | [trait 项][trait items] |
| `true`        | [布尔类型][boolean type]、[布尔表达式][boolean expressions]、[配置谓词][configuration predicates] |
| `try`         | [保留关键字][reserved keyword] |
| `type`        | [类型别名][type aliases] |
| `typeof`      | [保留关键字][reserved keyword] |
| `union`       | [联合体项][union items] |
| `unsafe`      | [不安全块][unsafe blocks]、[不安全属性][unsafe attributes]、[不安全模块][unsafe modules]、[不安全函数][unsafe functions]、[不安全外部块][unsafe external blocks]、[不安全外部函数][unsafe external functions]、[不安全外部静态项][unsafe external statics]、[不安全 trait][unsafe traits]、[不安全 trait 实现][unsafe trait implementations] |
| `unsized`     | [保留关键字][reserved keyword] |
| `use`         | [use 项][use items]、[use 约束][use bounds] |
| `virtual`     | [保留关键字][reserved keyword] |
| `where`       | [where 子句][where clauses] |
| `while`       | [谓词循环][predicate loops] |
| `yield`       | [保留关键字][reserved keyword] |

## 运算符与标点

| 符号 | 名称        | 用途 |
|--------|-------------|-----|
| `+`    | Plus        | [加法][arith]、[trait 约束][trait bounds]、[宏 Kleene matcher][macro Kleene matcher] |
| `-`    | Minus       | [减法][arith]、[取反][negation] |
| `*`    | Star        | [乘法][arith]、[解引用][dereference]、[裸指针][raw pointers]、[宏 Kleene matcher][macro Kleene matcher]、[glob 导入][glob imports] |
| `/`    | Slash       | [除法][arith] |
| `%`    | Percent     | [取余][arith] |
| `^`    | Caret       | [按位与逻辑 XOR][arith] |
| `!`    | Not         | [按位与逻辑 NOT][negation]、[宏调用][macro calls]、[内部属性][attributes]、[永不类型][never type]、[否定 impl][negative impls] |
| `&`    | And         | [按位与逻辑 AND][arith]、[借用][borrow]、[引用][references]、[引用模式][reference patterns] |
| `\|`   | Or | [按位与逻辑 OR][arith]、[闭包][closures]、[或模式][or patterns]、[if let]、[while let] |
| `&&`   | AndAnd      | [惰性 AND][lazy-bool]、[借用][borrow]、[引用][references]、[引用模式][reference patterns] |
| `\|\|` | OrOr | [惰性 OR][lazy-bool]、[闭包][closures] |
| `<<`   | Shl         | [左移][arith]、[嵌套泛型][generics] |
| `>>`   | Shr         | [右移][arith]、[嵌套泛型][generics] |
| `+=`   | PlusEq      | [加法赋值][compound] |
| `-=`   | MinusEq     | [减法赋值][compound] |
| `*=`   | StarEq      | [乘法赋值][compound] |
| `/=`   | SlashEq     | [除法赋值][compound] |
| `%=`   | PercentEq   | [取余赋值][compound] |
| `^=`   | CaretEq     | [按位 XOR 赋值][compound] |
| `&=`   | AndEq       | [按位 AND 赋值][compound] |
| `\|=`  | OrEq | [按位 OR 赋值][compound] |
| `<<=`  | ShlEq       | [左移赋值][compound] |
| `>>=`  | ShrEq       | [右移赋值][compound]、[嵌套泛型][generics] |
| `=`    | Eq          | [赋值][assignment]、[let 语句][let statements]、[属性][attributes]、各种类型定义 |
| `==`   | EqEq        | [等于][comparison] |
| `!=`   | Ne          | [不等于][comparison] |
| `>`    | Gt          | [大于][comparison]、[泛型][generics]、[路径][paths]、[use 约束][use bounds] |
| `<`    | Lt          | [小于][comparison]、[泛型][generics]、[路径][paths]、[use 约束][use bounds] |
| `>=`   | Ge          | [大于或等于][comparison]、[泛型][generics] |
| `<=`   | Le          | [小于或等于][comparison] |
| `@`    | At          | [子模式绑定][subpattern binding] |
| `.`    | Dot         | [字段访问][field]、[元组索引][tuple index]、[方法调用][method calls]、[await 表达式][await expressions] |
| `..`   | DotDot      | [范围表达式][expr.range]、[结构体表达式][struct expressions]、[剩余模式][rest pattern]、[范围模式][range patterns]、[结构体模式][struct patterns] |
| `...`  | DotDotDot   | [可变参数函数][variadic functions]、[范围模式][range patterns] |
| `..=`  | DotDotEq    | [闭区间范围表达式][expr.range]、[范围模式][range patterns] |
| `,`    | Comma       | 各种分隔符 |
| `;`    | Semi        | 各种项与语句的终止符、[数组表达式][array expressions]、[数组类型][array types] |
| `:`    | Colon       | 各种分隔符 |
| `::`   | PathSep     | [路径分隔符][paths] |
| `->`   | RArrow      | [函数][functions]、[闭包][closures]、[函数指针类型][function pointer type] |
| `=>`   | FatArrow    | [match 分支][match]、[宏][macros] |
| `<-`   | LArrow      | 左箭头符号自 Rust 1.0 之前就未再使用，但仍被当作单个 token。 |
| `#`    | Pound       | [属性][attributes]、[原始字符串字面量][raw string literals]、[原始字节字符串字面量][raw byte string literals]、[原始 C 字符串字面量][raw C string literals] |
| `$`    | Dollar      | [宏][macros] |
| `?`    | Question    | [try 传播表达式][question]、[宽松 trait 约束][relaxed trait bounds]、[宏 Kleene matcher][macro Kleene matcher] |
| `~`    | Tilde       | 波浪号运算符自 Rust 1.0 之前就未再使用，但其 token 仍可能被使用。 |

## 注释

| 注释  | 用途 |
|----------|-----|
| `//`     | [行注释][comments] |
| `//!`    | [内部行注释][comments] |
| `///`    | [外部行文档注释][comments] |
| `/*…*/`  | [块注释][comments] |
| `/*!…*/` | [内部块文档注释][comments] |
| `/**…*/` | [外部块文档注释][comments] |

## 其他 token

| Token        | 用途 |
|--------------|-----|
| `ident`      | [标识符][identifiers] |
| `r#ident`    | [原始标识符][raw identifiers] |
| `'ident`     | [生命周期与循环标签][lifetimes and loop labels] |
| `'r#ident`   | [原始生命周期与循环标签][raw lifetimes and loop labels] |
| `…u8`, `…i32`, `…f64`, `…usize`, … | [数字字面量][number literals] |
| `"…"`        | [字符串字面量][string literals] |
| `r"…"`, `r#"…"#`, `r##"…"##`, … | [原始字符串字面量][raw string literals] |
| `b"…"`       | [字节字符串字面量][byte string literals] |
| `br"…"`, `br#"…"#`, `br##"…"##`, … | [原始字节字符串字面量][raw byte string literals] |
| `'…'`        | [字符字面量][character literals] |
| `b'…'`       | [字节字面量][byte literals] |
| `c"…"`       | [C 字符串字面量][C string literals] |
| `cr"…"`, `cr#"…"#`, `cr##"…"##`, … | [原始 C 字符串字面量][raw C string literals] |

## 宏

| 语法                                     | 用途 |
|--------------------------------------------|-----|
| `ident!(…)`<br>`ident! {…}`<br>`ident![…]` | [宏调用][macro invocations] |
| `$ident`                                   | [宏元变量][macro metavariable] |
| `$ident:kind`                              | [宏 matcher fragment specifier][macro matcher fragment specifier] |
| `$(…)…`                                    | [宏重复][macro repetition] |

## 属性

| 语法     | 用途 |
|------------|-----|
| `#[meta]`  | [外部属性][outer attribute] |
| `#![meta]` | [内部属性][inner attribute] |

## 表达式

| 表达式                | 用途 |
|---------------------------|-----|
| `\|…\| expr`<br>`\|…\| -> Type { … }` | [闭包][closures] |
| `ident::…`                | [路径][paths] |
| `::crate_name::…`         | [显式 crate 路径][explicit crate paths] |
| `crate::…`                | [crate 相对路径][crate-relative paths] |
| `self::…`                 | [模块相对路径][module-relative paths] |
| `super::…`                | [父模块路径][parent module paths] |
| `Type::…`<br>`<Type as Trait>::ident` | [关联项][associated items] |
| `<Type>::…`               | 可用于无名称类型（如 `<&T>::…`、`<[T]>::…` 等）的[限定路径][qualified paths] |
| `Trait::method(…)`<br>`Type::method(…)`<br>`<Type as Trait>::method(…)` | [消歧义的方法调用][disambiguated method calls] |
| `method::<…>(…)`<br>`path::<…>` | [泛型实参][generic arguments]，即 turbofish |
| `()`                      | [单元][unit] |
| `(expr)`                  | [括号表达式][parenthesized expressions] |
| `(expr,)`                 | [单元素元组表达式][single-element tuple expressions] |
| `(expr, …)`               | [元组表达式][tuple expressions] |
| `expr(expr, …)`           | [调用表达式][call expressions] |
| `expr.0`, `expr.1`, …     | [元组索引表达式][tuple indexing expressions] |
| `expr.ident`              | [字段访问表达式][field access expressions] |
| `{…}`                     | [块表达式][block expressions] |
| `Type {…}`                | [结构体表达式][struct expressions] |
| `Type(…)`                 | [元组结构体构造函数][tuple struct constructors] |
| `[…]`                     | [数组表达式][array expressions] |
| `[expr; len]`             | [重复数组表达式][repeat array expressions] |
| `expr[..]`, `expr[a..]`, `expr[..b]`, `expr[a..b]`, `expr[a..=b]`, `expr[..=b]` | [数组与切片索引表达式][array and slice indexing expressions] |
| `if expr {…} else {…}`    | [if 表达式][if expressions] |
| `match expr { pattern => {…} }` | [match 表达式][match expressions] |
| `loop {…}`                | [无限循环表达式][infinite loop expressions] |
| `while expr {…}`          | [谓词循环表达式][predicate loop expressions] |
| `for pattern in expr {…}` | [迭代器循环][iterator loops] |
| `&expr`<br>`&mut expr`    | [借用表达式][borrow expressions] |
| `&raw const expr`<br>`&raw mut expr` | [裸借用表达式][raw borrow expressions] |
| `*expr`                   | [解引用表达式][dereference expressions] |
| `expr?`                   | [try 传播表达式][try propagation expressions] |
| `-expr`                   | [取反表达式][negation expressions] |
| `!expr`                   | [按位与逻辑 NOT 表达式][bitwise and logical NOT expressions] |
| `expr as Type`            | [类型强制转换表达式][type cast expressions] |

## 项

[项][Items] 是 crate 的组成部分。

| 项                          | 用途 |
|-------------------------------|-----|
| `mod ident;`<br>`mod ident {…}` | [模块][modules] |
| `use path;`                   | [use 声明][use declarations] |
| `fn ident(…) {…}`             | [函数][functions] |
| `type Type = Type;`           | [类型别名][type aliases] |
| `struct ident {…}`            | [结构体][structs] |
| `enum ident {…}`              | [枚举][enumerations] |
| `union ident {…}`             | [联合体][unions] |
| `trait ident {…}`             | [trait][traits] |
| `impl Type {…}`<br>`impl Type for Trait {…}` | [实现][implementations] |
| `const ident = expr;`         | [常量项][constant items] |
| `static ident = expr;`        | [静态项][static items] |
| `extern "C" {…}`              | [外部块][external blocks] |
| `fn ident<…>(…) …`<br>`struct ident<…> {…}`<br>`enum ident<…> {…}`<br>`impl<…> Type<…> {…}` | [泛型定义][generic definitions] |

## 类型表达式

[类型表达式][Type expressions] 用于引用类型。

| 类型                                  | 用途 |
|---------------------------------------|-----|
| `bool`, `u8`, `f64`, `str`, …         | [原语类型][primitive types] |
| `for<…>`                              | [高阶 trait 约束][higher-ranked trait bounds] |
| `T: TraitA + TraitB`                  | [trait 约束][trait bounds] |
| `T: 'a + 'b`                          | [生命周期约束][lifetime bounds] |
| `T: TraitA + 'a`                      | [trait 与生命周期约束][trait and lifetime bounds] |
| `T: ?Sized`                           | [宽松 trait 约束][relaxed trait bounds] |
| `[Type; len]`                         | [数组类型][array types] |
| `(Type, …)`                           | [元组类型][tuple types] |
| `[Type]`                              | [切片类型][slice types] |
| `(Type)`                              | [括号类型][parenthesized types] |
| `impl Trait`                          | [impl trait 类型][impl trait types]、[匿名类型参数][anonymous type parameters] |
| `dyn Trait`                           | [trait 对象类型][trait object types] |
| `ident`<br>`ident::…`                 | [类型路径][type paths]（可引用[结构体][structs]、[枚举][enumerations]、[联合体][unions]、[类型别名][type aliases]、[trait][traits]、[泛型][generics]等） |
| `Type<…>`<br>`Trait<…>`               | [泛型实参][generic arguments]（例如 `Vec<u8>`） |
| `Trait<ident = Type>`                 | [关联类型绑定][associated type bindings]（例如 `Iterator<Item = T>`） |
| `Trait<ident: …>`                     | [关联类型约束][associated type bounds]（例如 `Iterator<Item: Send>`） |
| `&Type`<br>`&mut Type`                | [引用类型][reference types] |
| `*mut Type`<br>`*const Type`          | [裸指针类型][raw pointer types] |
| `fn(…) -> Type`                       | [函数指针类型][function pointer types] |
| `_`                                   | [推断的类型][inferred type]、[推断的常量][inferred const] |
| `'_`                                  | [占位生命周期][placeholder lifetime] |
| `!`                                   | [永不类型][never type] |

## 模式

[模式][Patterns] 用于匹配值。

| 模式                           | 用途 |
|-----------------------------------|-----|
| `"foo"`, `'a'`, `123`, `2.4`, …   | [字面量模式][literal patterns] |
| `ident`                           | [标识符模式][identifier patterns] |
| `_`                               | [通配符模式][wildcard pattern] |
| `..`                              | [剩余模式][rest pattern] |
| `a..`, `..b`, `a..b`, `a..=b`, `..=b` | [范围模式][range patterns] |
| `&pattern`<br>`&mut pattern`      | [引用模式][reference patterns] |
| `path {…}`                        | [结构体模式][struct patterns] |
| `path(…)`                         | [元组结构体模式][tuple struct patterns] |
| `(pattern, …)`                    | [元组模式][tuple patterns] |
| `(pattern)`                       | [分组模式][grouped patterns] |
| `[pattern, …]`                    | [切片模式][slice patterns] |
| `CONST`, `Enum::Variant`, …       | [路径模式][path patterns] |

[`'static` lifetimes]: bound
[`if let` patterns]: expr.if.let
[`self` paths]: paths.qualifiers.mod-self
[`Self` type paths]: paths.qualifiers.type-self
[anonymous type parameters]: type.impl-trait.param
[arith]: expr.arith-logic
[array and slice indexing expressions]: expr.array.index
[array expressions]: expr.array
[array types]: type.array
[assembly operands]: asm.operand-type.supported-operands.in
[assignment]: expr.assign
[associated items]: items.associated
[associated type bindings]: paths.expr
[associated type bounds]: paths.expr
[async blocks]: expr.block.async
[async closures]: expr.closure.async
[async functions]: items.fn.async
[await expressions]: expr.await
[bitwise and logical NOT expressions]: expr.negate
[block expressions]: expr.block
[boolean expressions]: expr.literal
[boolean type]: type.bool
[borrow expressions]: expr.operator.borrow
[borrow]: expr.operator.borrow
[break expressions]: expr.loop.break
[byte literals]: lex.token.byte
[byte string literals]: lex.token.str-byte
[C string literals]: lex.token.str-c
[call expressions]: expr.call
[character literals]: lex.token.literal.char
[closure expressions]: expr.closure
[closures]: expr.closure
[comparison]: expr.cmp
[compound]: expr.compound-assign
[configuration predicates]: cfg
[const assembly operands]: asm.operand-type.supported-operands.const
[const blocks]: expr.block.const
[const functions]: const-eval.const-fn
[const generics]: items.generics.const
[const items]: items.const
[constant items]: items.const
[continue expressions]: expr.loop.continue
[crate-relative paths]: paths.qualifiers.crate
[dereference expressions]: expr.deref
[dereference]: expr.deref
[destructuring assignment]: expr.placeholder
[disambiguated method calls]: expr.call.desugar
[enumerations]: items.enum
[explicit crate paths]: paths.qualifiers.global-root
[extern crate]: items.extern-crate
[extern function pointer types]: type.fn-pointer.qualifiers
[extern function qualifier]: items.fn.extern
[external block functions]: items.extern.fn
[external block statics]: items.extern.static
[external blocks]: items.extern
[field access expressions]: expr.field
[field]: expr.field
[function pointer type]: type.fn-pointer
[function pointer types]: type.fn-pointer
[functions]: items.fn
[generic arguments]: items.generics
[generic definitions]: items.generics
[generics]: items.generics
[glob imports]: items.use.glob
[grouped patterns]: patterns.paren
[higher-ranked trait bounds]: bound.higher-ranked
[identifier patterns]: patterns.ident
[identifiers]: ident
[if expressions]: expr.if
[if let]: expr.if.let
[impl trait types]: type.impl-trait.return
[implementations]: items.impl
[inferred const]: items.generics.const.inferred
[inferred type]: type.inferred
[infinite loop expressions]: expr.loop.infinite
[infinite loops]: expr.loop.infinite
[inherent impls]: items.impl.inherent
[inner attribute]: attributes.inner
[iterator loops]: expr.loop.for
[lazy-bool]: expr.bool-logic
[let statements]: statement.let
[lifetime bounds]: bound.lifetime
[lifetimes and loop labels]: lex.token.life
[literal patterns]: patterns.literal
[macro calls]: macro.invocation
[macro invocations]: macro.invocation
[macro Kleene matcher]: macro.decl.repetition
[macro matcher fragment specifier]: macro.decl.meta.specifier
[macro metavariable]: macro.decl.meta
[macro repetition]: macro.decl.repetition
[macros by example]: macro.decl
[macros]: macro.decl
[match expressions]: expr.match
[match guards]: expr.match.guard
[match]: expr.match
[method calls]: expr.method
[module-relative paths]: paths.qualifiers.mod-self
[modules]: items.mod
[negation expressions]: expr.negate
[negation]: expr.negate
[negative impls]: items.impl
[never type]: type.never
[number literals]: lex.token.literal.num
[or patterns]: patterns.or
[outer attribute]: attributes.outer
[parent module paths]: paths.qualifiers.super
[parenthesized expressions]: expr.paren
[parenthesized types]: type.name.parenthesized
[path patterns]: patterns.path
[placeholder lifetime]: lifetime-elision.function.explicit-placeholder
[predicate loop expressions]: expr.loop.while
[predicate loops]: expr.loop.while
[primitive types]: type.kinds
[qualified paths]: paths.qualified
[question]: expr.try
[range patterns]: patterns.range
[raw assembly]: asm.options.supported-options.raw
[raw borrow expressions]: expr.borrow.raw
[raw borrow operator]: expr.borrow.raw
[raw byte string literals]: lex.token.str-byte-raw
[raw C string literals]: lex.token.str-c-raw
[raw identifiers]: ident.raw
[raw lifetimes and loop labels]: lex.token.life
[raw pointer type]: type.pointer.raw
[raw pointer types]: type.pointer.raw
[raw pointers]: type.pointer.raw
[raw string literals]: lex.token.literal.str-raw
[reference patterns]: patterns.ref
[reference types]: type.pointer.reference
[references]: type.pointer.reference
[relaxed trait bounds]: bound.sized
[repeat array expressions]: expr.array
[reserved keyword]: lex.keywords.reserved
[rest pattern]: patterns.rest
[return expressions]: expr.return
[self parameters]: items.fn.params.self-pat
[single-element tuple expressions]: expr.tuple
[slice patterns]: patterns.slice
[slice types]: type.slice
[static items]: items.static
[string literals]: lex.token.literal.str
[struct expressions]: expr.struct
[struct patterns]: patterns.struct
[structs]: items.struct
[subpattern binding]: patterns.ident.scrutinized
[super paths]: paths.qualifiers.super
[trait and lifetime bounds]: bound
[trait bounds]: bound
[trait implementations]: items.impl.trait
[trait impls]: items.impl.trait
[trait items]: items.traits
[trait object types]: type.trait-object
[trait objects]: type.trait-object
[traits]: items.traits
[try propagation expressions]: expr.try
[tuple expressions]: expr.tuple
[tuple index]: expr.tuple-index
[tuple indexing expressions]: expr.tuple-index
[tuple patterns]: patterns.tuple
[tuple struct constructors]: items.struct.tuple
[tuple struct patterns]: patterns.tuple-struct
[tuple types]: type.tuple
[type aliases]: items.type
[type cast expressions]: expr.as
[Type expressions]: type.name
[type paths]: type.name.path
[union items]: items.union
[unions]: items.union
[unit]: type.tuple.unit
[unsafe attributes]: attributes.safety
[unsafe blocks]: expr.block.unsafe
[unsafe external blocks]: unsafe.extern
[unsafe external functions]: items.extern.fn.safety
[unsafe external statics]: items.extern.static.safety
[unsafe functions]: unsafe.fn
[unsafe modules]: items.mod.unsafe
[unsafe trait implementations]: items.impl.trait.safety
[unsafe traits]: items.traits.safety
[use bounds]: bound.use
[use declarations]: items.use
[use items]: items.use
[variadic functions]: items.extern.variadic
[visibility]: vis
[where clauses]: items.generics.where
[while let]: expr.loop.while.let
[wildcard pattern]: patterns.wildcard
