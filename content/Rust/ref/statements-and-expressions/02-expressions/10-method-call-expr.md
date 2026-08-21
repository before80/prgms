+++
title = "10-方法调用表达式"
date = 2026-08-18T08:45:00+08:00
weight = 53
type = "docs"
description = "方法调用表达式 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/expressions/method-call-expr.html](https://doc.rust-lang.org/reference/expressions/method-call-expr.html)

r[expr.method]
# 方法调用表达式

r[expr.method.syntax]
```grammar,expressions
MethodCallExpression -> Expression `.` PathExprSegment `(`CallParams? `)`
```

r[expr.method.intro]
*方法调用*由一个表达式（*接收者*）、一个点号、一个表达式路径段，以及一个由圆括号括起的表达式列表组成。

r[expr.method.target]
方法调用会解析为特定 trait 上的关联[方法][methods]：若左侧的确切 `self` 类型已知，则静态分派到该方法；若左侧表达式是间接的 [trait 对象](../../type-system/01-types/16-trait-object/)，则动态分派。

```rust
let pi: Result<f32, _> = "3.14".parse();
let log_pi = pi.unwrap_or(1.0).log(2.72);
## assert!(1.14 < log_pi && log_pi < 1.15)
```

r[expr.method.autoref-deref]
查找方法调用时，接收者可能被自动解引用或借用以便调用方法。这比其它函数需要更复杂的查找过程，因为可能有多个可调用的方法。使用如下过程：

r[expr.method.candidate-receivers]
第一步是构建候选接收者类型列表。通过对接收者表达式的类型反复[解引用][dereference]，将遇到的每个类型加入列表，最后再尝试一次数组[不定长强制转换][unsized coercion]，若成功则把结果类型也加入列表。

r[expr.method.candidate-receivers-refs]
然后，对每个候选类型 `T`，在 `T` 之后立即把 `&T` 和 `&mut T` 加入列表。

例如，若接收者类型为 `Box<[i32;2]>`，则候选类型为 `Box<[i32;2]>`、`&Box<[i32;2]>`、`&mut Box<[i32;2]>`、`[i32; 2]`（通过解引用）、`&[i32; 2]`、`&mut [i32; 2]`、`[i32]`（通过不定长强制转换）、`&[i32]`，最后是 `&mut [i32]`。

r[expr.method.candidate-search]
然后，对每个候选类型 `T`，在下列位置查找以该类型为接收者的[可见][visible]方法：

1. `T` 的固有方法（直接在 `T` 上实现的方法）。
1. 由 `T` 所实现的[可见][visible] trait 提供的任何方法。若 `T` 是类型参数，则首先查找 `T` 上 trait 约束所提供的方法，然后再查找作用域中其余方法。

> **注意**
> 查找按类型顺序进行，偶尔会产生出人意料的结果。下面的代码会打印 “In trait impl!”，因为会先查找 `&self` 方法，从而在找到结构体的 `&mut self` 方法之前就找到了 trait 方法。
>
> ```rust
> struct Foo {}
>
> trait Bar {
>   fn bar(&self);
> }
>
> impl Foo {
>   fn bar(&mut self) {
>     println!("In struct impl!")
>   }
> }
>
> impl Bar for Foo {
>   fn bar(&self) {
>     println!("In trait impl!")
>   }
> }
>
> fn main() {
>   let mut f = Foo{};
>   f.bar();
> }
> ```

r[expr.method.ambiguous-target]
若这导致多个可能的候选，则为错误，必须将接收者[转换][disambiguate call]为合适的接收者类型才能进行方法调用。

r[expr.method.receiver-constraints]
该过程不考虑接收者的可变性或生命周期，也不考虑方法是否为 `unsafe`。一旦查找到方法，若因上述一个（或多个）原因无法调用，结果就是编译器错误。

r[expr.method.ambiguous-search]
若某一步出现多个可能的方法，例如将泛型方法或 trait 视为相同，则为编译器错误。这些情况需要使用[消除歧义的函数调用语法][disambiguating function call syntax]来调用方法或函数。

r[expr.method.edition2021]
> [!EDITION-2021]
> 在 2021 edition 之前，查找可见方法时，若候选接收者类型是[数组类型][array type]，则会忽略标准库 [`IntoIterator`] trait 所提供的方法。
>
> 此用途所采用的 edition 由表示方法名的词法单元决定。
>
> 这一特例将来可能会被移除。

> **警告**
> 对于 [trait 对象][trait objects]，若存在与某个 trait 方法同名的固有方法，则在方法调用表达式中尝试调用该方法会给出编译器错误。作为替代，可以使用[消除歧义的函数调用语法][disambiguating function call syntax]来调用，此时调用的是 trait 方法，而不是固有方法。没有办法调用该固有方法。只要不要在 trait 对象上定义与 trait 方法同名的固有方法，就不会有问题。

[visible]: ../visibility-and-privacy.md
[array type]: ../types/array.md
[trait objects]: ../types/trait-object.md
[disambiguate call]: call-expr.md#disambiguating-function-calls
[disambiguating function call syntax]: call-expr.md#disambiguating-function-calls
[dereference]: operator-expr.md#the-dereference-operator
[methods]: ../items/associated-items.md#methods
[unsized coercion]: ../type-coercions.md#unsized-coercions
[`IntoIterator`]: std::iter::IntoIterator
