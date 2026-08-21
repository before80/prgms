+++
title = "06-Trait 与生命周期约束"
date = 2026-08-18T08:45:00+08:00
weight = 89
type = "docs"
description = "Trait 与生命周期约束 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/trait-bounds.html](https://doc.rust-lang.org/reference/trait-bounds.html)

r[bound]
# Trait 与生命周期约束

r[bound.syntax]
```grammar,miscellaneous
Bounds -> Bound ( `+` Bound )* `+`?

Bound -> Lifetime | TraitBound | UseBound

TraitBound ->
      ( `?` | ForLifetimes )? TypePath
    | `(` ( `?` | ForLifetimes )? TypePath `)`

LifetimeBounds -> ( Lifetime `+` )* Lifetime?

Lifetime ->
      LIFETIME_OR_LABEL
    | `'static`
    | `'_`

UseBound -> `use` UseBoundGenericArgs

UseBoundGenericArgs ->
      `<` `>`
    | `<` ( UseBoundGenericArg `,`)* UseBoundGenericArg `,`? `>`

UseBoundGenericArg ->
      Lifetime
    | IDENTIFIER
    | `Self`
```

r[bound.intro]
[Trait] 与生命周期约束为[泛型项][generic]提供了一种限制哪些类型和生命周期可用作其参数的方式。约束可以在 [where 子句][where clause]中施加于任何类型。对于某些常见情形还有更短的形式：

* 写在声明[泛型参数][generic]之后的约束：`fn f<A: Copy>() {}` 与 `fn f<A>() where A: Copy {}` 相同。
* 在 trait 声明中作为[超 trait][supertraits]：`trait Circle : Shape {}` 等价于 `trait Circle where Self : Shape {}`。
* 在 trait 声明中作为[关联类型][associated types]上的约束：`trait A { type B: Copy; }` 等价于 `trait A where Self::B: Copy { type B; }`。

r[bound.satisfaction]
使用某项时必须满足该项上的约束。在对泛型项进行类型检查和借用检查时，约束可用于确定某个类型实现了某个 trait。例如，给定 `Ty: Trait`

* 在泛型函数体内，可以对 `Ty` 值调用 `Trait` 中的方法。同样可以使用 `Trait` 上的关联常量。
* 可以使用来自 `Trait` 的关联类型。
* 带有 `T: Trait` 约束的泛型函数和类型可以使用 `Ty` 作为 `T`。

```rust
## type Surface = i32;
trait Shape {
    fn draw(&self, surface: Surface);
    fn name() -> &'static str;
}

fn draw_twice<T: Shape>(surface: Surface, sh: T) {
    sh.draw(surface);           // 可以调用方法，因为 T: Shape
    sh.draw(surface);
}

fn copy_and_draw_twice<T: Copy>(surface: Surface, sh: T) where T: Shape {
    let shape_copy = sh;        // 不会移动 sh，因为 T: Copy
    draw_twice(surface, sh);    // 可以使用泛型函数，因为 T: Shape
}

struct Figure<S: Shape>(S, S);

fn name_figure<U: Shape>(
    figure: Figure<U>,          // 类型 Figure<U> 是合式的，因为 U: Shape
) {
    println!(
        "Figure of two {}",
        U::name(),              // 可以使用关联函数
    );
}
```

r[bound.trivial]
不使用该项参数或[高阶生命周期][higher-ranked lifetimes]的约束在定义该项时检查。此类约束为假是错误。

r[bound.special]
在使用该项时，即使该使用并未提供具体类型，也会对某些泛型类型检查 [`Copy`]、[`Clone`] 和 [`Sized`] 约束。将 `Copy` 或 `Clone` 作为可变引用、[trait 对象][trait object]或[切片][slice]上的约束是错误。将 `Sized` 作为 trait 对象或切片上的约束是错误。

```rust
struct A<'a, T>
where
    i32: Default,           // 允许，但没有用
    i32: Iterator,          // 错误：`i32` 不是迭代器
    &'a mut T: Copy,        // （使用时）错误：未满足 trait 约束
    [T]: Sized,             // （使用时）错误：大小在编译时无法得知
{
    f: &'a T,
}
struct UsesA<'a, T>(A<'a, T>);
```

r[bound.trait-object]
Trait 与生命周期约束也用于命名 [trait 对象][trait objects]。

r[bound.sized]
## `?Sized`

`?` 仅用于放宽[类型参数][type parameters]或[关联类型][associated types]上隐式的 [`Sized`] trait 约束。`?Sized` 不得用作其他类型的约束。

r[bound.lifetime]
## 生命周期约束

r[bound.lifetime.intro]
生命周期约束可以施加于类型或其他生命周期。

r[bound.lifetime.outlive-lifetime]
约束 `'a: 'b` 通常读作 `'a` *长于* `'b`。`'a: 'b` 意味着 `'a` 至少与 `'b` 一样长，因此只要 `&'b ()` 有效，引用 `&'a ()` 就有效。

```rust
fn f<'a, 'b>(x: &'a i32, mut y: &'b i32) where 'a: 'b {
    y = x;                      // &'a i32 是 &'b i32 的子类型，因为 'a: 'b
    let r: &'b &'a i32 = &&0;   // &'b &'a i32 是合式的，因为 'a: 'b
}
```

r[bound.lifetime.outlive-type]
`T: 'a` 意味着 `T` 的所有生命周期参数都长于 `'a`。例如，若 `'a` 是不受约束的生命周期参数，则 `i32: 'static` 和 `&'static str: 'a` 得到满足，但 `Vec<&'a ()>: 'static` 不满足。

r[bound.higher-ranked]
## 高阶 trait 约束

r[bound.higher-ranked.syntax]
```grammar,miscellaneous
ForLifetimes -> `for` GenericParams
```

r[bound.higher-ranked.intro]
Trait 约束可以在生命周期上是 *高阶* 的。这些约束指定对 *所有* 生命周期都成立的约束。例如，诸如 `for<'a> &'a T: PartialEq<i32>` 的约束会要求类似如下的实现

```rust
## struct T;
impl<'a> PartialEq<i32> for &'a T {
    // ...
##    fn eq(&self, other: &i32) -> bool {true}
}
```

然后就可以将任意生命周期的 `&'a T` 与 `i32` 进行比较。

此处只能使用高阶约束，因为该引用的生命周期短于函数上任何可能的生命周期参数：

```rust
fn call_on_ref_zero<F>(f: F) where for<'a> F: Fn(&'a i32) {
    let zero = 0;
    f(&zero);
}
```

r[bound.higher-ranked.trait]
高阶生命周期也可以就写在 trait 之前：唯一的区别是生命周期参数的[作用域][hrtb-scopes]，它只延伸到紧随其后的 trait 的末尾，而不是整个约束。下面的函数与上一个等价。

```rust
fn call_on_ref_zero<F>(f: F) where F: for<'a> Fn(&'a i32) {
    let zero = 0;
    f(&zero);
}
```

r[bound.implied]
## 隐含约束

r[bound.implied.intro]
类型要合式所要求的生命周期约束有时会被推断出来。

```rust
fn requires_t_outlives_a<'a, T>(x: &'a T) {}
```

要使类型 `&'a T` 合式，类型参数 `T` 必须长于 `'a`。这会被推断出来，因为函数签名包含类型 `&'a T`，而该类型仅在 `T: 'a` 成立时才有效。

r[bound.implied.context]
会对函数的所有参数和输出添加隐含约束。在 `requires_t_outlives_a` 内部，即使你没有显式指定，也可以假定 `T: 'a` 成立：

```rust
fn requires_t_outlives_a_not_implied<'a, T: 'a>() {}

fn requires_t_outlives_a<'a, T>(x: &'a T) {
    // 这段可以编译，因为 `T: 'a` 由
    // 引用类型 `&'a T` 隐含。
    requires_t_outlives_a_not_implied::<'a, T>();
}
```

```rust
## fn requires_t_outlives_a_not_implied<'a, T: 'a>() {}
fn not_implied<'a, T>() {
    // 这段会报错，因为 `T: 'a` 并未由
    // 函数签名隐含。
    requires_t_outlives_a_not_implied::<'a, T>();
}
```

r[bound.implied.trait]
只有生命周期约束会被隐含，trait 约束仍然必须显式添加。因此下面的例子会导致错误：

```rust
use std::fmt::Debug;
struct IsDebug<T: Debug>(T);
// 错误[E0277]：`T` 未实现 `Debug`
fn doesnt_specify_t_debug<T>(x: IsDebug<T>) {}
```

r[bound.implied.def]
生命周期约束也会为类型定义以及任何类型的 impl 块推断：

```rust
struct Struct<'a, T> {
    // 这要求 `T: 'a` 才能合式，
    // 由编译器推断。
    field: &'a T,
}

enum Enum<'a, T> {
    // 这要求 `T: 'a` 才能合式，
    // 由编译器推断。
    //
    // 注意即使只使用 `Enum::OtherVariant`，
    // 也要求 `T: 'a`。
    SomeVariant(&'a T),
    OtherVariant,
}

trait Trait<'a, T: 'a> {}

// 这会报错，因为 `T: 'a` 并未由 impl 头中
// 的任何类型隐含。
//     impl<'a, T> Trait<'a, T> for () {}

// 这段可以编译，因为 `T: 'a` 由自身类型 `&'a T` 隐含。
impl<'a, T> Trait<'a, T> for &'a T {}
```

r[bound.use]
## Use 约束

某些约束列表可以包含 `use<..>` 约束，以控制哪些泛型参数被 `impl Trait` [抽象返回类型][abstract return type]捕获。更多细节参见[精确捕获][precise capturing]。

[abstract return type]: types/impl-trait.md#abstract-return-types
[arrays]: types/array.md
[associated types]: items/associated-items.md#associated-types
[hrtb-scopes]: names/scopes.md#higher-ranked-trait-bound-scopes
[supertraits]: items/traits.md#supertraits
[generic]: items/generics.md
[higher-ranked lifetimes]: #higher-ranked-trait-bounds
[precise capturing]: types/impl-trait.md#precise-capturing
[slice]: types/slice.md
[Trait]: items/traits.md#trait-bounds
[trait object]: types/trait-object.md
[trait objects]: types/trait-object.md
[type parameters]: types/parameters.md
[where clause]: items/generics.md#where-clauses
