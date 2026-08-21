+++
title = "17-impl Trait 类型"
date = 2026-08-18T08:45:00+08:00
weight = 82
type = "docs"
description = "impl Trait 类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types/impl-trait.html](https://doc.rust-lang.org/reference/types/impl-trait.html)

r[type.impl-trait]
# impl Trait 类型

r[type.impl-trait.syntax]
```grammar,types
ImplTraitType -> `impl` Bounds?

ImplTraitTypeOneBound -> `impl` TraitBound?
```

r[type.impl-trait.intro]
`impl Trait` 提供了指定实现特定 trait 的未命名但具体的类型的方式。它可以出现在两类位置：参数位置（在此它可以作为函数的匿名类型参数）和返回位置（在此它可以作为抽象返回类型）。

```rust
trait Trait {}
## impl Trait for () {}

// 参数位置：匿名类型参数
fn foo(arg: impl Trait) {
}

// 返回位置：抽象返回类型
fn bar() -> impl Trait {
}
```

r[type.impl-trait.bounds]
必须至少有一个 trait 约束，不能有多于一个 `use<..>` 约束，也不能有多于一个退出约束（例如 `?Sized`）。

r[type.impl-trait.param]
## 匿名类型参数

> **注意**
> 这通常称为「参数位置的 impl Trait」。（此处用「参数」更准确，但「参数位置的 impl Trait」是该特性开发期间使用的措辞，并且在实现的部分地方仍然保留。）

r[type.impl-trait.param.intro]
函数可以使用 `impl` 后跟一组 trait 约束，将某个参数声明为具有匿名类型。调用者必须提供满足该匿名类型参数所声明约束的类型，而函数只能使用该匿名类型参数的 trait 约束所提供的方法。

例如，以下两种形式几乎等价：

```rust
trait Trait {}

// 泛型类型参数
fn with_generic_type<T: Trait>(arg: T) {
}

// 参数位置的 impl Trait
fn with_impl_trait(arg: impl Trait) {
}
```

r[type.impl-trait.param.generic]
也就是说，参数位置的 `impl Trait` 是类似 `<T: Trait>` 的泛型类型参数的语法糖，只不过该类型是匿名的，并且不出现在 [GenericParams] 列表中。

> **注意**
> 对于函数参数，泛型类型参数和 `impl Trait` 并不完全等价。使用诸如 `<T: Trait>` 的泛型参数时，调用者可以选择在调用点用 [GenericArgs] 显式指定 `T` 的泛型实参，例如 `foo::<usize>(1)`。将参数从其中一种改为另一种可能构成对该函数调用者的破坏性变更，因为这会改变泛型实参的数量。

r[type.impl-trait.return]
## 抽象返回类型

> **注意**
> 这通常称为「返回位置的 impl Trait」。

r[type.impl-trait.return.intro]
函数可以使用 `impl Trait` 来返回抽象返回类型。这些类型代表另一个具体类型，调用者只能使用所指定 `Trait` 声明的方法。

r[type.impl-trait.return.constraint-body]
函数的每个可能返回值都必须解析为同一个具体类型。

返回位置的 `impl Trait` 允许函数返回未装箱的抽象类型。这在[闭包][closures]和迭代器中特别有用。例如，闭包具有唯一、无法写出的类型。此前，从函数返回闭包的唯一方式是使用 [trait 对象][trait object]：

```rust
fn returns_closure() -> Box<dyn Fn(i32) -> i32> {
    Box::new(|x| x + 1)
}
```

这可能因堆分配和动态分派而产生性能开销。无法完整指定闭包的类型，只能使用 `Fn` trait。这意味着必须使用 trait 对象。然而，有了 `impl Trait`，可以更简单地写成：

```rust
fn returns_closure() -> impl Fn(i32) -> i32 {
    |x| x + 1
}
```

这样也避免了使用装箱 trait 对象的缺点。

类似地，迭代器的具体类型可能变得非常复杂，会纳入链式调用中所有先前迭代器的类型。返回 `impl Iterator` 意味着函数只将其返回类型约束为 `Iterator` trait，而不显式指定所涉及的所有其他迭代器类型。

r[type.impl-trait.return-in-trait]
## Trait 与 trait 实现中返回位置的 `impl Trait`

r[type.impl-trait.return-in-trait.intro]
Trait 中的函数也可以使用 `impl Trait` 作为匿名关联类型的语法。

r[type.impl-trait.return-in-trait.desugaring]
Trait 中关联函数返回类型里的每个 `impl Trait` 都会被脱糖为匿名关联类型。实现中函数签名所出现的返回类型用于确定该关联类型的值。

r[type.impl-trait.generic-captures]
## 捕获

每个返回位置 `impl Trait` 抽象类型背后都有某个隐藏的具体类型。要使该具体类型使用某个泛型参数，该泛型参数必须被该抽象类型 *捕获*。

r[type.impl-trait.generic-capture.auto]
## 自动捕获

r[type.impl-trait.generic-capture.auto.intro]
返回位置的 `impl Trait` 抽象类型会自动捕获所有作用域内的泛型参数，包括泛型类型、const 和生命周期参数（包括高阶的）。

r[type.impl-trait.generic-capture.edition2024]
> [!EDITION-2024]
> 在 2024 edition 之前，对于自由函数以及固有 impl 的关联函数和方法，未出现在抽象返回类型约束中的泛型生命周期参数不会被自动捕获。

r[type.impl-trait.generic-capture.precise]
## 精确捕获

r[type.impl-trait.generic-capture.precise.use]
返回位置 `impl Trait` 抽象类型所捕获的泛型参数集合可以用 [`use<..>` 约束][`use<..>` bound]显式控制。若存在该约束，则只有列在 `use<..>` 约束中的泛型参数会被捕获。例如：

```rust
fn capture<'a, 'b, T>(x: &'a (), y: T) -> impl Sized + use<'a, T> {
  //                                      ~~~~~~~~~~~~~~~~~~~~~~~
  //                                     仅捕获 `'a` 和 `T`。
  (x, y)
}
```

r[type.impl-trait.generic-capture.precise.constraint-single]
目前，约束列表中最多只能有一个 `use<..>` 约束，所有作用域内的类型和 const 泛型参数都必须包含在内，并且出现在抽象类型其他约束中的所有生命周期参数也都必须包含在内。

r[type.impl-trait.generic-capture.precise.constraint-lifetime]
在 `use<..>` 约束中，任何出现的生命周期参数必须位于所有类型和 const 泛型参数之前，并且若省略生命周期（`'_`）在其他方面被允许出现在该 `impl Trait` 返回类型中，则也可以出现。

r[type.impl-trait.generic-capture.precise.constraint-param-impl-trait]
由于所有作用域内的类型参数都必须按名称包含，因此 `use<..>` 约束不能用于使用参数位置 `impl Trait` 的项的签名，因为这些项的作用域中有匿名类型参数。

r[type.impl-trait.generic-capture.precise.constraint-in-trait]
Trait 定义中关联函数里出现的任何 `use<..>` 约束都必须包含该 trait 的所有泛型参数，包括该 trait 隐式的 `Self` 泛型类型参数。

## 泛型与返回位置 `impl Trait` 的差异

在参数位置，`impl Trait` 在语义上与泛型类型参数非常相似。然而，二者在返回位置有显著差别。与泛型类型参数不同，使用 `impl Trait` 时由函数选择返回类型，调用者不能选择返回类型。

函数：

```rust
## trait Trait {}
fn foo<T: Trait>() -> T {
    // ...
## panic!()
}
```

允许调用者确定返回类型 `T`，函数返回该类型。

函数：

```rust
## trait Trait {}
## impl Trait for () {}
fn foo() -> impl Trait {
    // ...
}
```

不允许调用者确定返回类型。相反，由函数选择返回类型，但只承诺它会实现 `Trait`。

r[type.impl-trait.constraint]
## 限制

`impl Trait` 只能作为非 `extern` 函数的参数或返回类型出现。它不能是 `let` 绑定的类型、字段类型，也不能出现在类型别名内部。

[`use<..>` bound]: ../trait-bounds.md#use-bounds
[closures]: closure.md
[trait object]: trait-object.md
