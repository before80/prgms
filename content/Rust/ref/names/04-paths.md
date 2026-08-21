+++
title = "04-路径"
date = 2026-08-18T08:45:00+08:00
weight = 99
type = "docs"
description = "路径 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/paths.html](https://doc.rust-lang.org/reference/paths.html)

r[paths]
# 路径

r[paths.intro]
*路径*（path）是由一个或多个路径段（path segment）组成的序列，各段之间以 `::` 记号分隔。路径用于引用[条目][items]、值、[类型][types]、[宏][macros]以及[属性][attributes]。

以下是仅由标识符段构成的简单路径的两个例子：

<!-- ignore: syntax fragment -->
```rust
x;
x::y::z;
```

## 路径的种类

r[paths.simple]
### 简单路径

r[paths.simple.syntax]
```grammar,paths
SimplePath ->
    `::`? SimplePathSegment (`::` SimplePathSegment)*

SimplePathSegment ->
    IDENTIFIER | `super` | `self` | `crate` | `$crate`
```

r[paths.simple.intro]
简单路径用于[可见性][visibility]标记、[属性][attributes]、[宏][mbe]以及 [`use`] 条目中。例如：

```rust
use std::io::{self, Write};
mod m {
    #[clippy::cyclomatic_complexity = "0"]
    pub (in super) fn f1() {}
}
```

r[paths.expr]
### 表达式中的路径

r[paths.expr.syntax]
```grammar,paths
PathInExpression ->
    `::`? PathExprSegment (`::` PathExprSegment)*

PathExprSegment ->
    PathIdentSegment (`::` GenericArgs)?

PathIdentSegment ->
    IDENTIFIER | `super` | `self` | `Self` | `crate` | `$crate`

GenericArgs ->
      `<` GenericArgList? `>`
    | `(` TypeList? `)` (`->` TypeNoBounds)?

GenericArgList ->
    ( GenericArg `,` )* GenericArg `,`?

TypeList ->
    ( Type `,` )* Type `,`?

GenericArg ->
    Lifetime | Type | GenericArgsConst | GenericArgsBinding | GenericArgsBounds

GenericArgsConst ->
      BlockExpression
    | LiteralExpression
    | `-` LiteralExpression
    | SimplePathSegment

GenericArgsBinding ->
    TypePathSegment `=` Type

GenericArgsBounds ->
    TypePathSegment `:` Bounds?
```

r[paths.expr.intro]
表达式中的路径允许指定带有泛型参数的路径。它们用于[表达式][expressions]和[模式][patterns]中的多种位置。

r[paths.expr.turbofish]
在泛型参数的起始 `<` 之前必须使用 `::` 记号，以避免与小于运算符产生歧义。这种写法俗称 “turbofish” 语法。

```rust
(0..10).collect::<Vec<_>>();
Vec::<u8>::with_capacity(1024);
```

r[paths.expr.argument-order]
泛型参数的顺序受限：先是生命周期参数，然后是类型参数，再是常量参数，最后是等式约束。

r[paths.expr.complex-const-params]
常量参数必须用花括号括起，除非它们是[字面量][literal]、[推断常量][inferred const]，或单段路径。[推断常量][inferred const]不得用花括号括起。

```rust
mod m {
    pub const C: usize = 1;
}
const C: usize = m::C;
fn f<const N: usize>() -> [u8; N] { [0; N] }

let _ = f::<1>(); // 字面量。
let _: [_; 1] = f::<_>(); // 推断常量。
let _: [_; 1] = f::<(((_)))>(); // 推断常量。
let _ = f::<C>(); // 单段路径。
let _ = f::<{ m::C }>(); // 多段路径必须用花括号括起。
```

```rust
fn f<const N: usize>() -> [u8; N] { [0; _] }
let _: [_; 1] = f::<{ _ }>();
//                    ^ ERROR `_` not allowed here
```

> **注意**
> 在泛型参数列表中，[推断常量][inferred const]按[推断类型][InferredType]进行解析，但在语义上会被当作一种单独的[常量泛型参数][const generic argument]。

r[paths.expr.impl-trait-params]
与 `impl Trait` 类型对应的合成类型参数是隐式的，不能显式指定。

r[paths.qualified]
## 限定路径

r[paths.qualified.syntax]
```grammar,paths
QualifiedPathInExpression -> QualifiedPathType (`::` PathExprSegment)+

QualifiedPathType -> `<` Type (`as` TypePath)? `>`

QualifiedPathInType -> QualifiedPathType (`::` TypePathSegment)+
```

r[paths.qualified.intro]
完全限定路径用于消除[特质实现][trait implementations]中路径的歧义，以及指定[规范路径](#canonical-paths)。在类型说明中使用时，它支持下文给出的类型语法。

```rust
struct S;
impl S {
    fn f() { println!("S"); }
}
trait T1 {
    fn f() { println!("T1 f"); }
}
impl T1 for S {}
trait T2 {
    fn f() { println!("T2 f"); }
}
impl T2 for S {}
S::f();  // 调用固有实现。
<S as T1>::f();  // 调用 T1 特质函数。
<S as T2>::f();  // 调用 T2 特质函数。
```

r[paths.type]
### 类型中的路径

r[paths.type.syntax]
```grammar,paths
TypePath -> `::`? TypePathSegment (`::` TypePathSegment)*

TypePathSegment -> PathIdentSegment (`::`? GenericArgs)?
```

r[paths.type.intro]
类型路径用于类型定义、特质约束以及限定路径中。

r[paths.type.turbofish]
虽然允许在泛型参数之前使用 `::` 记号，但并不强制要求，因为这里不像 [PathInExpression] 那样存在歧义。

```rust
## mod ops {
##     pub struct Range<T> {f1: T}
##     pub trait Index<T> {}
##     pub struct Example<'a> {f1: &'a i32}
## }
## struct S;
impl ops::Index<ops::Range<usize>> for S { /*...*/ }
fn i<'a>() -> impl Iterator<Item = ops::Example<'a>> {
    // ...
##    const EXAMPLE: Vec<ops::Example<'static>> = Vec::new();
##    EXAMPLE.into_iter()
}
type G = std::boxed::Box<dyn std::ops::FnOnce(isize) -> isize>;
```

r[paths.qualifiers]
## 路径限定符

路径可以带有多种前导限定符，以改变其解析方式。

> **注意**
> [`use` 声明][`use` declarations]对 `self`、`super`、`crate` 和 `$crate` 有额外的行为和限制。

r[paths.qualifiers.global-root]
### `::`

r[paths.qualifiers.global-root.intro]
以 `::` 开头的路径被视为*全局路径*（global path），其各段的解析起点因版本而异。路径中的每个标识符都必须解析到某个条目。

r[paths.qualifiers.global-root.edition2018]
> [!EDITION-2018]
> 在 2015 版中，标识符从“crate 根”（2018 版中的 `crate::`）开始解析；该根包含多种不同的条目，包括外部 crate、诸如 `std` 或 `core` 之类的默认 crate，以及 crate 顶层的条目（包括 `use` 导入）。
>
> 从 2018 版开始，以 `::` 开头的路径从[外部 prelude][extern prelude] 中的 crate 开始解析。也就是说，其后必须跟某个 crate 的名称。

```rust
pub fn foo() {
    // 在 2018 版中，这通过外部 prelude 访问 `std`。
    // 在 2015 版中，这通过 crate 根访问 `std`。
    let now = ::std::time::Instant::now();
    println!("{:?}", now);
}
```

```rust
// 2015 版
mod a {
    pub fn foo() {}
}
mod b {
    pub fn foo() {
        ::a::foo(); // 调用 `a` 的 foo 函数
        // 在 Rust 2018 中，`::a` 会被解释为名为 `a` 的 crate。
    }
}
## fn main() {}
```

r[paths.qualifiers.mod-self]
### `self`

r[paths.qualifiers.mod-self.intro]
`self` 使路径相对于当前模块进行解析。

r[paths.qualifiers.mod-self.restriction]
`self` 只能用作路径的第一段（且前面没有 `::`），或用作最后一段（前面带有 `::`）。

r[paths.qualifiers.mod-self.trailing]
当 `self` 作为路径的最后一段出现时，它引用由前一段命名的实体。前面的路径必须解析为[模块][module]、[枚举][enumeration]或[特质][trait]。

```rust
mod m {
    pub enum E { V1 }
    pub trait Tr {}
    pub(in crate::m::self) fn g() {} // OK：模块可以是 `self` 的父级。
}
type Ty = m::E::self; // OK：枚举可以是 `self` 的父级。
fn f<T: m::Tr::self>() {} // OK：特质可以是 `self` 的父级。
## fn main() { let _: Ty = m::E::V1; }
```

```rust
struct S;
type Ty = S::self; // ERROR：结构体不能是 `self` 的父级。
## fn main() {}
```

> **注意**
> 关于 `use` 声明中 `self` 的额外规则，参见 [items.use.self]。

r[paths.qualifiers.self-pat]
在方法体中，仅由单个 `self` 段构成的路径会解析为该方法的 self 参数。

```rust
fn foo() {}
fn bar() {
    self::foo();
}
struct S(bool);
impl S {
  fn baz(self) {
        self.0;
    }
}
## fn main() {}
```

r[paths.qualifiers.type-self]
### `Self`

r[paths.qualifiers.type-self.intro]
大写的 `Self` 用于引用当前正在实现或定义的类型。它可以用于以下情形：

r[paths.qualifiers.type-self.trait]
* 在[特质][trait]定义中，它引用实现该特质的类型。

r[paths.qualifiers.type-self.impl]
* 在[实现][implementation]中，它引用正在被实现的类型。在实现元组或单元[结构体][struct]时，它也引用[值命名空间][value namespace]中的构造函数。

r[paths.qualifiers.type-self.type]
* 在[结构体][struct]、[枚举][enumeration]或[联合体][union]的定义中，它引用正在被定义的类型。该定义不允许无限递归（必须存在间接层）。

r[paths.qualifiers.type-self.scope]
`Self` 的作用域行为类似于泛型参数；更多细节参见 [`Self` 作用域][`Self` scope] 一节。

r[paths.qualifiers.type-self.allowed-positions]
`Self` 只能用作第一段，且前面不能有 `::`。

r[paths.qualifiers.type-self.no-generics]
`Self` 路径不能包含泛型参数（例如 `Self::<i32>`）。

```rust
trait T {
    type Item;
    const C: i32;
    // `Self` 将是实现 `T` 的任意类型。
    fn new() -> Self;
    // `Self::Item` 将是实现中的类型别名。
    fn f(&self) -> Self::Item;
}
struct S;
impl T for S {
    type Item = i32;
    const C: i32 = 9;
    fn new() -> Self {           // `Self` 是类型 `S`。
        S
    }
    fn f(&self) -> Self::Item {  // `Self::Item` 是类型 `i32`。
        Self::C                  // `Self::C` 是常量值 `9`。
    }
}

// `Self` 在特质定义的泛型中处于作用域内，
// 用于引用正在定义的类型。
trait Add<Rhs = Self> {
    type Output;
    // `Self` 也可以引用被实现类型的
    // 关联条目。
    fn add(self, rhs: Rhs) -> Self::Output;
}

struct NonEmptyList<T> {
    head: T,
    // 结构体可以引用自身（只要不是
    // 无限递归）。
    tail: Option<Box<Self>>,
}
```

r[paths.qualifiers.super]
### `super`

r[paths.qualifiers.super.intro]
路径中的 `super` 解析为父模块。

r[paths.qualifiers.super.allowed-positions]
它只能用于路径的前导段，可能出现在初始的 `self` 段之后。

```rust
mod a {
    pub fn foo() {}
}
mod b {
    pub fn foo() {
        super::a::foo(); // 调用 a 的 foo 函数
    }
}
## fn main() {}
```

r[paths.qualifiers.super.repetition]
在第一个 `super` 或 `self` 之后，可以重复多次使用 `super`，以引用祖先模块。

```rust
mod a {
    fn foo() {}

    mod b {
        mod c {
            fn foo() {
                super::super::foo(); // 调用 a 的 foo 函数
                self::super::super::foo(); // 调用 a 的 foo 函数
            }
        }
    }
}
## fn main() {}
```

r[paths.qualifiers.crate]
### `crate`

r[paths.qualifiers.crate.intro]
`crate` 使路径相对于当前 crate 进行解析。

r[paths.qualifiers.crate.allowed-positions]
`crate` 只能用作第一段，且前面不能有 `::`。

```rust
fn foo() {}
mod a {
    fn bar() {
        crate::foo();
    }
}
## fn main() {}
```

r[paths.qualifiers.macro-crate]
### `$crate`

r[paths.qualifiers.macro-crate.allowed-positions]
[`$crate`] 仅用于[宏转写器][macro transcribers]中，并且只能用作第一段，且前面不能有 `::`。

r[paths.qualifiers.macro-crate.hygiene]
无论宏在哪个 crate 中被调用，[`$crate`] 都会展开为一条路径，用于访问定义该宏的 crate 顶层的条目。

```rust
pub fn increment(x: u32) -> u32 {
    x + 1
}

#[macro_export]
macro_rules! inc {
    ($x:expr) => ( $crate::increment($x) )
}
## fn main() { }
```

r[paths.canonical]
## 规范路径

r[paths.canonical.intro]
在模块或实现中定义的每个条目都有一条*规范路径*（canonical path），对应于它在其 crate 内的定义位置。

r[paths.canonical.alias]
指向这些条目的所有其他路径都是别名。

r[paths.canonical.def]
规范路径定义为*路径前缀*（path prefix）再加上该条目自身定义的路径段。

r[paths.canonical.non-canonical]
[实现][Implementations]和 [use 声明][use declarations]没有规范路径，尽管实现中定义的条目有规范路径。在块表达式中定义的条目没有规范路径。在没有规范路径的模块中定义的条目也没有规范路径。在实现中定义的关联条目，若该实现所引用的条目没有规范路径——例如作为被实现的类型、被实现的特质、类型参数或类型参数上的约束——则这些关联条目也没有规范路径。

r[paths.canonical.module-prefix]
模块的路径前缀是该模块的规范路径。

r[paths.canonical.bare-impl-prefix]
对于裸实现，路径前缀是被实现条目的规范路径，并用<span class="parenthetical">尖括号（`<>`）</span>括起。

r[paths.canonical.trait-impl-prefix]
对于[特质实现][trait implementations]，路径前缀是被实现条目的规范路径，后跟 `as`，再跟特质的规范路径，整体用<span class="parenthetical">尖括号（`<>`）</span>括起。

r[paths.canonical.local-canonical-path]
规范路径仅在给定 crate 内有意义。跨 crate 不存在全局命名空间；条目的规范路径仅标识它在该 crate 内的身份。

```rust
// 注释显示该条目的规范路径。

mod a { // crate::a
    pub struct Struct; // crate::a::Struct

    pub trait Trait { // crate::a::Trait
        fn f(&self); // crate::a::Trait::f
    }

    impl Trait for Struct {
        fn f(&self) {} // <crate::a::Struct as crate::a::Trait>::f
    }

    impl Struct {
        fn g(&self) {} // <crate::a::Struct>::g
    }
}

mod without { // crate::without
    fn canonicals() { // crate::without::canonicals
        struct OtherStruct; // None

        trait OtherTrait { // None
            fn g(&self); // None
        }

        impl OtherTrait for OtherStruct {
            fn g(&self) {} // None
        }

        impl OtherTrait for crate::a::Struct {
            fn g(&self) {} // None
        }

        impl crate::a::Trait for OtherStruct {
            fn f(&self) {} // None
        }
    }
}

## fn main() {}
```

[`$crate`]: macro.decl.hygiene.crate
[implementations]: items/implementations.md
[items]: items.md
[literal]: expressions/literal-expr.md
[use declarations]: items/use-declarations.md
[`Self` scope]: names/scopes.md#self-scope
[`use`]: items/use-declarations.md
[attributes]: attributes.md
[const generic argument]: items.generics.const.argument
[enumeration]: items/enumerations.md
[expressions]: expressions.md
[extern prelude]: names/preludes.md#extern-prelude
[implementation]: items/implementations.md
[inferred const]: items.generics.const.inferred
[macro transcribers]: macros-by-example.md
[macros]: macros.md
[mbe]: macros-by-example.md
[module]: items/modules.md
[patterns]: patterns.md
[struct]: items/structs.md
[trait implementations]: items/implementations.md#trait-implementations
[trait]: items/traits.md
[traits]: items/traits.md
[types]: types.md
[union]: items/unions.md
[`use` declarations]: items/use-declarations.md
[value namespace]: names/namespaces.md
[visibility]: visibility-and-privacy.md
