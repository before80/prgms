+++
title = "12-实现"
date = 2026-08-18T08:45:00+08:00
weight = 29
type = "docs"
description = "实现 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/items/implementations.html](https://doc.rust-lang.org/reference/items/implementations.html)

r[items.impl]
# 实现

r[items.impl.syntax]
```grammar,items
Implementation -> InherentImpl | TraitImpl

InherentImpl ->
    `impl` GenericParams? Type WhereClause? `{`
        InnerAttribute*
        AssociatedItem*
    `}`

TraitImpl ->
    `unsafe`? `impl` GenericParams? `!`? TypePath `for` Type
    WhereClause?
    `{`
        InnerAttribute*
        AssociatedItem*
    `}`
```

r[items.impl.intro]
*实现*是将项与*实现类型*关联起来的项。实现用关键字 `impl` 定义，并包含属于正在被实现的类型的实例或静态属于该类型的函数。

r[items.impl.kinds]
实现有两种：

- 固有实现
- [trait] 实现

r[items.impl.inherent]
## 固有实现

r[items.impl.inherent.intro]
固有实现定义为 `impl` 关键字、泛型类型声明、到名义类型的路径、where 子句，以及一组用花括号括起的可关联项的序列。

r[items.impl.inherent.implementing-type]
该名义类型称为*实现类型*，可关联项是该实现类型的*关联项*。

r[items.impl.inherent.associated-items]
固有实现将其所含项关联到实现类型。

r[items.impl.inherent.associated-items.allowed-items]
固有实现可以包含[关联函数][associated functions]（包括[方法][methods]）和[关联常量][associated constants]。

r[items.impl.inherent.type-alias]
它们不能包含关联类型别名。

r[items.impl.inherent.associated-item-path]
到关联项的[路径][path]是到实现类型的任意路径，后跟关联项的标识符作为最后的路径分量。

r[items.impl.inherent.coherence]
一个类型也可以有多个固有实现。实现类型必须与原始类型定义在同一 crate 中定义。

``` rust
pub mod color {
    pub struct Color(pub u8, pub u8, pub u8);

    impl Color {
        pub const WHITE: Color = Color(255, 255, 255);
    }
}

mod values {
    use super::color::Color;
    impl Color {
        pub fn red() -> Color {
            Color(255, 0, 0)
        }
    }
}

pub use self::color::Color;
fn main() {
    // 到实现类型的实际路径，且 impl 在同一模块中。
    color::Color::WHITE;

    // 不同模块中的 impl 块仍通过到该类型的路径访问。
    color::Color::red();

    // 到实现类型的再导出路径也可以。
    Color::red();

    // 不行，因为 `values` 中的 use 不是 pub。
    // values::Color::red();
}
```

r[items.impl.trait]
## Trait 实现

r[items.impl.trait.intro]
*trait 实现*的定义类似于固有实现，只不过可选的泛型类型声明之后跟着一个 [trait]、关键字 `for`，然后是到名义类型的路径。

<!-- To understand this, you have to back-reference to the previous section. :( -->

r[items.impl.trait.implemented-trait]
该 trait 称为*被实现的 trait*。实现类型实现被实现的 trait。

r[items.impl.trait.def-requirement]
trait 实现必须定义被实现 trait 所声明的所有非默认关联项，可以重新定义被实现 trait 所定义的默认关联项，并且不能定义任何其他项。

r[items.impl.trait.associated-item-path]
到关联项的路径是 `<`，后跟到实现类型的路径，再跟 `as`，再跟到 trait 的路径，再跟 `>` 作为一个路径分量，然后是关联项的路径分量。

r[items.impl.trait.safety]
[不安全 trait][Unsafe traits] 要求 trait 实现以 `unsafe` 关键字开头。

```rust
## #[derive(Copy, Clone)]
## struct Point {x: f64, y: f64};
## type Surface = i32;
## struct BoundingBox {x: f64, y: f64, width: f64, height: f64};
## trait Shape { fn draw(&self, s: Surface); fn bounding_box(&self) -> BoundingBox; }
## fn do_draw_circle(s: Surface, c: Circle) { }
struct Circle {
    radius: f64,
    center: Point,
}

impl Copy for Circle {}

impl Clone for Circle {
    fn clone(&self) -> Circle { *self }
}

impl Shape for Circle {
    fn draw(&self, s: Surface) { do_draw_circle(s, *self); }
    fn bounding_box(&self) -> BoundingBox {
        let r = self.radius;
        BoundingBox {
            x: self.center.x - r,
            y: self.center.y - r,
            width: 2.0 * r,
            height: 2.0 * r,
        }
    }
}
```

r[items.impl.trait.coherence]
### Trait 实现的连贯性

r[items.impl.trait.coherence.intro]
若孤儿规则检查失败，或存在重叠的实现实例，则认为 trait 实现不连贯。

r[items.impl.trait.coherence.overlapping]
当实现所针对的 trait 有非空交集，并且这些实现可以用同一类型实例化时，两个 trait 实现重叠。 <!-- This is probably wrong? Source: No two implementations can be instantiable with the same set of types for the input type parameters. -->

r[items.impl.trait.orphan-rule]
#### 孤儿规则

r[items.impl.trait.orphan-rule.intro]
*孤儿规则*规定，仅当该 trait 或实现中至少一种类型在当前 crate 中定义时，才允许该 trait 实现。它防止不同 crate 之间出现冲突的 trait 实现，是确保连贯性的关键。

孤儿实现是为外部类型实现外部 trait 的实现。若它们被自由允许，两个 crate 就可能以不兼容的方式为同一类型实现同一 trait，从而造成添加或更新依赖项会因冲突实现而破坏编译的局面。

孤儿规则使库作者可以为其 trait 添加新实现，而不必担心会破坏下游代码。没有这些限制，库就不能添加诸如 `impl<T: Display> MyTrait for T` 的实现，因为可能与下游实现冲突。

r[items.impl.trait.orphan-rule.def]
给定 `impl<P1..=Pn> Trait<T1..=Tn> for T0`，仅当下列至少一项为真时，该 `impl` 才合法：

- `Trait` 是[局部 trait][local trait]
- 下列全部成立
  - 类型 `T0..=Tn` 中至少有一个必须是[局部类型][local type]。令 `Ti` 为第一个这样的类型。
  - [未覆盖的类型][uncovered type]参数 `P1..=Pn` 不得出现在 `T0..Ti` 中（不包括 `Ti`）

r[items.impl.trait.uncovered-param]
只有*未覆盖*类型参数的出现受到限制。

r[items.impl.trait.fundamental]
注意，就连贯性而言，[基本类型][fundamental types]是特殊的。`Box<T>` 中的 `T` 不被视为被覆盖，且 `Box<LocalType>` 被视为局部的。

r[items.impl.generics]
## 泛型实现

r[items.impl.generics.intro]
实现可以带[泛型参数][generic parameters]，它们可以在实现的其余部分使用。实现参数直接写在 `impl` 关键字之后。

```rust
## trait Seq<T> { fn dummy(&self, _: T) { } }
impl<T> Seq<T> for Vec<T> {
    /* ... */
}
impl Seq<bool> for u32 {
    /* 把该整数当作位序列来处理 */
}
```

r[items.impl.generics.use]
若泛型参数至少在下列位置之一出现一次，则它*约束*该实现：

* 被实现的 trait（若有）
* 实现类型
* 作为某个类型的[约束][bounds]中的[关联类型][associated type]，且该类型包含另一个约束该实现的参数

r[items.impl.generics.constrain]
类型参数和常量参数必须始终约束该实现。若生命周期用在关联类型中，则生命周期必须约束该实现。

构成约束的情况的例子：

```rust
## trait Trait{}
## trait GenericTrait<T> {}
## trait HasAssocType { type Ty; }
## struct Struct;
## struct GenericStruct<T>(T);
## struct ConstGenericStruct<const N: usize>([(); N]);
// T 通过作为 GenericTrait 的实参来约束。
impl<T> GenericTrait<T> for i32 { /* ... */ }

// T 通过作为 GenericStruct 的实参来约束
impl<T> Trait for GenericStruct<T> { /* ... */ }

// 同理，N 通过作为 ConstGenericStruct 的实参来约束
impl<const N: usize> Trait for ConstGenericStruct<N> { /* ... */ }

// T 通过出现在类型 `U` 的约束中的关联类型来约束，而 `U`
// 本身是约束该 trait 的泛型参数。
impl<T, U> GenericTrait<U> for u32 where U: HasAssocType<Ty = T> { /* ... */ }

// 与上一个类似，只不过类型是 `(U, isize)`。`U` 出现在包含
// `T` 的类型内部，而不是该类型本身。
impl<T, U> GenericStruct<U> where (U, isize): HasAssocType<Ty = T> { /* ... */ }
```

不构成约束的情况的例子：

```rust
// 其余这些是错误的，因为它们有不约束的类型或常量参数。

// T 完全没有出现，因此不约束。
impl<T> Struct { /* ... */ }

// N 由于同样的原因不约束。
impl<const N: usize> Struct { /* ... */ }

// 在实现内部使用 T 并不约束该 impl。
impl<T> Struct {
    fn uses_t(t: &T) { /* ... */ }
}

// T 用作 U 的约束中的关联类型，但 U 并不约束。
impl<T, U> Struct where U: HasAssocType<Ty = T> { /* ... */ }

// T 用在约束中，但不是作为关联类型，因此它不约束。
impl<T, U> GenericTrait<U> for u32 where U: GenericTrait<T> {}
```

允许的不构成约束的生命周期参数的例子：

```rust
## struct Struct;
impl<'a> Struct {}
```

不允许的不构成约束的生命周期参数的例子：

```rust
## struct Struct;
## trait HasAssocType { type Ty; }
impl<'a> HasAssocType for Struct {
    type Ty = &'a Struct;
}
```

r[items.impl.attributes]
## 实现上的属性

实现可以在 `impl` 关键字之前包含外部[属性][attributes]，并在包含关联项的花括号内包含内部[属性][attributes]。内部属性必须出现在任何关联项之前。此处有意义的属性有 [`cfg`]、[`deprecated`]、[`doc`] 和 [lint 检查属性][the lint check attributes]。

[trait]: traits.md
[associated constants]: associated-items.md#associated-constants
[associated functions]: associated-items.md#associated-functions-and-methods
[associated type]: associated-items.md#associated-types
[attributes]: ../attributes.md
[bounds]: ../trait-bounds.md
[`cfg`]: ../conditional-compilation.md
[`deprecated`]: ../attributes/diagnostics.md#the-deprecated-attribute
[`doc`]: ../../rustdoc/the-doc-attribute.html
[generic parameters]: generics.md
[methods]: associated-items.md#methods
[path]: ../paths.md
[the lint check attributes]: ../attributes/diagnostics.md#lint-check-attributes
[Unsafe traits]: traits.md#unsafe-traits
[local trait]: ../glossary.md#local-trait
[local type]: ../glossary.md#local-type
[fundamental types]: ../glossary.md#fundamental-type-constructors
[uncovered type]: ../glossary.md#uncovered-type
