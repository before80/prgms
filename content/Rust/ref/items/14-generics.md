+++
title = "14-泛型参数"
date = 2026-08-18T08:45:00+08:00
weight = 31
type = "docs"
description = "泛型参数 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/items/generics.html](https://doc.rust-lang.org/reference/items/generics.html)

r[items.generics]
# 泛型参数

r[items.generics.syntax]
```grammar,items
GenericParams -> `<` ( GenericParam (`,` GenericParam)* `,`? )? `>`

GenericParam -> OuterAttribute* ( LifetimeParam | TypeParam | ConstParam )

LifetimeParam -> Lifetime ( `:` LifetimeBounds? )?

TypeParam -> IDENTIFIER ( `:` Bounds? )? ( `=` Type )?

ConstParam ->
    `const` IDENTIFIER `:` Type
    ( `=` ( BlockExpression | IDENTIFIER | `-`?LiteralExpression ) )?
```

r[items.generics.syntax.intro]
[函数][Functions]、[类型别名][type aliases]、[结构体][structs]、[枚举][enumerations]、[联合体][unions]、[trait][traits] 和[实现][implementations]都可以由类型、常量和生命周期*参数化*。这些参数列在尖<span class="parenthetical">括号（`<...>`）</span>中，通常紧跟在项名之后、定义之前。对于没有名称的实现，它们直接出现在 `impl` 之后。

r[items.generics.syntax.decl-order]
泛型参数的顺序被限制为先是生命周期参数，然后类型参数和常量参数可以混排。

r[items.generics.syntax.duplicate-params]
同一参数名不得在 [GenericParams] 列表中声明超过一次。

带有类型、常量和生命周期参数的项的一些例子：

```rust
fn foo<'a, T>() {}
trait A<U> {}
struct Ref<'a, T> where T: 'a { r: &'a T }
struct InnerArray<T, const N: usize>([T; N]);
struct EitherOrderWorks<const N: bool, U>(U);
```

r[items.generics.syntax.scope]
泛型参数在声明它们的项定义内处于作用域中。它们不在函数体内声明的项的作用域中，如[项声明][item declarations]所述。更多细节参见[泛型参数作用域][generic parameter scopes]。

r[items.generics.builtin-generic-types]
[引用][References]、[原始指针][raw pointers]、[数组][arrays]、[切片][slices]、[元组][tuples]和[函数指针][function pointers]也具有生命周期或类型参数，但并不用路径语法来指称。

r[items.generics.invalid-lifetimes]
`'_` 和 `'static` 不是合法的生命周期参数名。

r[items.generics.const]
### 常量泛型

r[items.generics.const.intro]
*常量泛型参数*允许项在常量值上是泛型的。

r[items.generics.const.namespace]
该 const 标识符在[值命名空间][value namespace]中为该常量参数引入一个名称，并且该项的所有实例都必须用给定类型的值来实例化。

r[items.generics.const.allowed-types]
常量参数唯一允许的类型是 `u8`、`u16`、`u32`、`u64`、`u128`、`usize`、`i8`、`i16`、`i32`、`i64`、`i128`、`isize`、`char` 和 `bool`。

r[items.generics.const.use]
常量参数可以在[常量项][const item]可以使用的任何地方使用，例外是当用在[类型][type]或[数组重复表达式][array repeat expression]中时，它必须是独立的（如下所述）。也就是说，它们允许出现在下列位置：

1. 作为应用于构成该项签名一部分的任何类型的常量。
2. 作为用于定义[关联常量][associated const]的常量表达式的一部分，或作为[关联类型][associated type]的参数。
3. 作为该项中任何函数体内任何运行时表达式中的值。
4. 作为该项中任何函数体内所用任何类型的参数。
5. 作为该项中任何字段的类型的一部分。

```rust
// 可以使用常量泛型参数的例子。

// 用在项自身的签名中。
fn foo<const N: usize>(arr: [i32; N]) {
    // 用作函数体内的类型。
    let x: [i32; N];
    // 用作表达式。
    println!("{}", N * 2);
}

// 用作结构体的字段。
struct Foo<const N: usize>([i32; N]);

impl<const N: usize> Foo<N> {
    // 用作关联常量。
    const CONST: usize = N * 4;
}

trait Trait {
    type Output;
}

impl<const N: usize> Trait for Foo<N> {
    // 用作关联类型。
    type Output = [i32; N];
}
```

```rust
// 不能使用常量泛型参数的例子。
fn foo<const N: usize>() {
    // 不能用在函数体内的项定义中。
    const BAD_CONST: [usize; N] = [1; N];
    static BAD_STATIC: [usize; N] = [1; N];
    fn inner(bad_arg: [usize; N]) {
        let bad_value = N * 2;
    }
    type BadAlias = [usize; N];
    struct BadStruct([usize; N]);
}
```

r[items.generics.const.standalone]
进一步的限制是，常量参数在[类型][type]或[数组重复表达式][array repeat expression]中只能作为独立实参出现。在那些上下文中，它们只能用作单段[路径表达式][path expression]，可能位于[块][block]内（例如 `N` 或 `{N}`）。也就是说，它们不能与其他表达式组合。

```rust
// 不能使用常量参数的例子。

// 不允许在类型中的其他表达式里组合，例如这里
// 返回类型中的算术表达式。
fn bad_function<const N: usize>() -> [u8; {N + 1}] {
    // 数组重复表达式同样不允许。
    [1; {N + 1}]
}
```

r[items.generics.const.argument]
[路径][path]中的常量实参指定该项要使用的常量值。

r[items.generics.const.argument.const-expr]
该实参必须要么是[推断常量][inferred const]，要么是赋予该常量参数的类型的[常量表达式][const expression]。除非它是单路径段（一个 [IDENTIFIER]）或[字面量][literal]（可能带有前导 `-` token），否则该常量表达式必须是[块表达式][block]（用花括号包围）。

> **注意**
> 这一语法限制是必要的，以避免在解析类型内部的表达式时需要无限向前看。

```rust
struct S<const N: i64>;
const C: i64 = 1;
fn f<const N: i64>() -> S<N> { S }

let _ = f::<1>(); // 字面量。
let _ = f::<-1>(); // 负字面量。
let _ = f::<{ 1 + 2 }>(); // 常量表达式。
let _ = f::<C>(); // 单段路径。
let _ = f::<{ C + 1 }>(); // 常量表达式。
let _: S<1> = f::<_>(); // 推断常量。
let _: S<1> = f::<(((_)))>(); // 推断常量。
```

> **注意**
> 在泛型实参列表中，[推断常量][inferred const]被解析为[推断类型][InferredType]，但随后在语义上被当作一种单独的[常量泛型实参][const generic argument]。

r[items.generics.const.inferred]
在期望常量实参的地方，可以使用 `_`（可选地被任意数量的匹配圆括号包围），称为*推断常量*（[路径规则][paths.expr.complex-const-params]、[数组表达式规则][expr.array.length-restriction]）。这会请求编译器在可能的情况下根据周围信息推断该常量实参。

```rust
fn make_buf<const N: usize>() -> [u8; N] {
    [0; _]
    //  ^ 推断 `N`。
}
let _: [u8; 1024] = make_buf::<_>();
//                             ^ 推断 `1024`。
```

> **注意**
> [推断常量][inferred const]在语义上不是[表达式][Expression]，因此不被花括号内接受。
>
> ```rust
> fn f<const N: usize>() -> [u8; N] { [0; _] }
> let _: [_; 1] = f::<{ _ }>();
> //                    ^ 错误：这里不允许 `_`
> ```

r[items.generics.const.inferred.constraint]
推断常量不能用在项签名中。

```rust
fn f<const N: usize>(x: [u8; N]) -> [u8; _] { x }
//                                       ^ 错误：不允许
```

r[items.generics.const.type-ambiguity]
当泛型实参既可以解析为类型实参也可以解析为常量实参而产生歧义时，它总是被解析为类型。把该实参放在块表达式中可以强制将其解释为常量实参。

<!-- TODO: Rewrite the paragraph above to be in terms of namespaces, once namespaces are introduced, and it is clear which namespace each parameter lives in. -->

```rust
type N = u32;
struct Foo<const N: usize>;
// 下面是错误的，因为 `N` 被解释为类型别名 `N`。
fn foo<const N: usize>() -> Foo<N> { todo!() } // 错误
// 可以用花括号包围来强制将其解释为 `N`
// 常量参数，从而修复：
fn bar<const N: usize>() -> Foo<{ N }> { todo!() } // 可以
```

r[items.generics.const.variance]
与类型参数和生命周期参数不同，常量参数可以声明而不在参数化项内部使用，[泛型实现][generic implementations]中所述的实现除外：

```rust
// 可以
struct Foo<const N: usize>;
enum Bar<const M: usize> { A, B }

// 错误：未使用的参数
struct Baz<T>;
struct Biz<'a>;
struct Unconstrained;
impl<const N: usize> Unconstrained {}
```

r[items.generics.const.exhaustiveness]
在解析 trait 约束义务时，确定该约束是否满足时不考虑常量参数的所有实现是否穷尽。例如，在下列代码中，即使 `bool` 类型的所有可能常量值都已实现，trait 约束仍未满足，因而仍是错误：

```rust
struct Foo<const B: bool>;
trait Bar {}
impl Bar for Foo<true> {}
impl Bar for Foo<false> {}

fn needs_bar(_: impl Bar) {}
fn generic<const B: bool>() {
    let v = Foo::<B>;
    needs_bar(v); // 错误：未满足 trait 约束 `Foo<B>: Bar`
}
```

r[items.generics.where]
## Where 子句

r[items.generics.where.syntax]
```grammar,items
WhereClause -> `where` ( WhereClauseItem `,` )* WhereClauseItem?

WhereClauseItem ->
      LifetimeWhereClauseItem
    | TypeBoundWhereClauseItem

LifetimeWhereClauseItem -> Lifetime `:` LifetimeBounds?

TypeBoundWhereClauseItem -> ForLifetimes? Type `:` Bounds?
```

r[items.generics.where.intro]
*Where 子句*提供另一种在类型和生命周期参数上指定约束的方式，以及在并非类型参数的类型上指定约束的方式。

r[items.generics.where.higher-ranked-lifetimes]
`for` 关键字可用于引入[高阶生命周期][higher-ranked lifetimes]。它只允许 [LifetimeParam] 参数。

```rust
struct A<T>
where
    T: Iterator,            // 可以用 A<T: Iterator> 代替
    T::Item: Copy,          // 关联类型上的约束
    String: PartialEq<T>,   // 在 `String` 上的约束，使用了类型参数
    i32: Default,           // 允许，但没有用处
{
    f: T,
}
```

r[items.generics.attributes]
## 属性

泛型生命周期参数和类型参数允许带[属性][attributes]。没有内置属性会在此位置做任何事，不过自定义 derive 属性可能赋予其含义。

此例展示使用自定义 derive 属性来修改泛型参数的含义。

<!-- ignore: requires proc macro derive -->
```rust
// 假定 MyFlexibleClone 的 derive 声明了它能理解
// `my_flexible_clone` 属性。
#[derive(MyFlexibleClone)]
struct Foo<#[my_flexible_clone(unbounded)] H> {
    a: *const H
}
```

[array repeat expression]: ../expressions/array-expr.md
[arrays]: ../types/array.md
[slices]: ../types/slice.md
[associated const]: associated-items.md#associated-constants
[associated type]: associated-items.md#associated-types
[attributes]: ../attributes.md
[block]: ../expressions/block-expr.md
[const contexts]: ../const_eval.md#const-context
[const expression]: ../const_eval.md#constant-expressions
[const generic argument]: items.generics.const.argument
[const item]: constant-items.md
[enumerations]: enumerations.md
[functions]: functions.md
[function pointers]: ../types/function-pointer.md
[generic implementations]: implementations.md#generic-implementations
[generic parameter scopes]: ../names/scopes.md#generic-parameter-scopes
[higher-ranked lifetimes]: ../trait-bounds.md#higher-ranked-trait-bounds
[implementations]: implementations.md
[inferred const]: items.generics.const.inferred
[item declarations]: ../statements.md#item-declarations
[item]: ../items.md
[literal]: ../expressions/literal-expr.md
[path]: ../paths.md
[path expression]: ../expressions/path-expr.md
[raw pointers]: ../types/pointer.md#raw-pointers-const-and-mut
[references]: ../types/pointer.md#shared-references-
[structs]: structs.md
[tuples]: ../types/tuple.md
[trait object]: ../types/trait-object.md
[traits]: traits.md
[type aliases]: type-aliases.md
[type]: ../types.md
[unions]: unions.md
[value namespace]: ../names/namespaces.md
