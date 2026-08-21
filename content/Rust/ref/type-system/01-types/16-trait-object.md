+++
title = "16-Trait 对象类型"
date = 2026-08-18T08:45:00+08:00
weight = 81
type = "docs"
description = "Trait 对象类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types/trait-object.html](https://doc.rust-lang.org/reference/types/trait-object.html)

r[type.trait-object]
# Trait 对象类型

r[type.trait-object.syntax]
```grammar,types
TraitObjectType -> Bounds[^bare-2021] | `dyn`[^dyn-2018] Bounds?

TraitObjectTypeOneBound -> TraitBound[^bare-2021] | `dyn`[^dyn-2018] TraitBound?
```

[^bare-2021]: 参见 [type.trait-object.syntax-edition2021]。
[^dyn-2018]: 参见 [type.trait-object.syntax-edition2018]。

r[type.trait-object.intro]
*trait 对象* 是实现了一组 trait 的另一种类型的不透明值。这组 trait 由一个 [dyn 兼容][dyn compatible]的 *基础 trait* 加上任意数量的[自动 trait][auto traits]组成。

r[type.trait-object.impls]
Trait 对象实现基础 trait、其自动 trait，以及基础 trait 的任何[超 trait][supertraits]。

r[type.trait-object.bounds]
必须至少有一个 trait 约束，不能有多于一个非自动 trait，不能有多于一个生命周期，并且不允许退出约束（例如 `?Sized`）和 `use<..>` 约束。

例如，给定 trait `Trait`，以下都是 trait 对象：

* `dyn Trait`
* `dyn Trait + Send`
* `dyn Trait + Send + Sync`
* `dyn Trait + 'static`
* `dyn Trait + Send + 'static`
* `dyn Trait +`
* `dyn 'static + Trait`.
* `dyn (Trait)`

r[type.trait-object.syntax-edition2021]
> [!EDITION-2021]
> 在 2021 edition 之前，可以省略 `dyn` 关键字。在 2021 edition 及之后，从语义上要求使用 `dyn` 关键字。

r[type.trait-object.syntax-edition2018]
> [!EDITION-2018]
> 在 2015 edition 中，`dyn` 后面必须跟着 [PathIdentSegment]、[LIFETIME_TOKEN]、`for`、`(` 或 `?`，才会被解释为关键字而不是普通标识符。
>
> 最值得注意的是，`dyn`、`dyn::T` 和 `dyn<T>` 都会被当作类型路径。因此，若你想要一个以 `::module::Trait` 为 trait 的 trait 对象类型，需要把路径放在括号中，写作 `dyn (::module::Trait)`。
>
> 从 2018 edition 开始，`dyn` 是真正的关键字，不允许出现在路径中，因此不再需要括号。

r[type.trait-object.alias]
两个 trait 对象类型互为别名，当且仅当基础 trait 互为别名、自动 trait 集合相同、且生命周期约束相同。例如，`dyn Trait + Send + UnwindSafe` 与 `dyn Trait + UnwindSafe + Send` 相同。

r[type.trait-object.unsized]
由于值的具体类型是不透明的，trait 对象是[动态大小类型][dynamically sized types]。与所有 <abbr title="dynamically sized types">DST</abbr> 一样，trait 对象用在某种指针之后；例如 `&dyn SomeTrait` 或 `Box<dyn SomeTrait>`。每个指向 trait 对象的指针实例包含：

 - 一个指向实现了 `SomeTrait` 的类型 `T` 的实例的指针
 - 一张 _虚方法表_，通常简称为 _vtable_，其中对于 `SomeTrait` 及其[超 trait][supertraits]中 `T` 所实现的每个方法，都包含一个指向 `T` 的实现的指针（即函数指针）。

Trait 对象的目的是允许方法的「迟绑定」。在 trait 对象上调用方法会在运行时进行虚分派：也就是说，从 trait 对象的 vtable 中加载一个函数指针并间接调用。每个 vtable 条目的实际实现可以因对象而异。

一个 trait 对象的例子：

```rust
trait Printable {
    fn stringify(&self) -> String;
}

impl Printable for i32 {
    fn stringify(&self) -> String { self.to_string() }
}

fn print(a: Box<dyn Printable>) {
    println!("{}", a.stringify());
}

fn main() {
    print(Box::new(10) as Box<dyn Printable>);
}
```

在这个例子中，trait `Printable` 作为 trait 对象出现在 `print` 的类型签名以及 `main` 中的强制转换表达式中。

r[type.trait-object.lifetime-bounds]
## Trait 对象的生命周期约束

由于 trait 对象可以包含引用，这些引用的生命周期需要作为 trait 对象的一部分来表达。该生命周期写作 `Trait + 'a`。存在一些[默认值][defaults]，使得这个生命周期通常可以被推断为一个合理的选择。

[auto traits]: ../special-types-and-traits.md#auto-traits
[defaults]: ../lifetime-elision.md#default-trait-object-lifetimes
[dyn compatible]: ../items/traits.md#dyn-compatibility
[dynamically sized types]: ../dynamically-sized-types.md
[supertraits]: ../items/traits.md#supertraits
