+++
title = "11-Trait"
date = 2026-08-18T08:45:00+08:00
weight = 28
type = "docs"
description = "Trait — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/items/traits.html](https://doc.rust-lang.org/reference/items/traits.html)

r[items.traits]
# Trait

r[items.traits.syntax]
```grammar,items
Trait ->
    `unsafe`? `trait` IDENTIFIER GenericParams? ( `:` Bounds? )? WhereClause?
    `{`
        InnerAttribute*
        AssociatedItem*
    `}`
```

r[items.traits.intro]
*trait* 描述类型可以实现的抽象接口。该接口由[关联项][associated items]组成，关联项有三种：

- [函数](associated-items.md#associated-functions-and-methods)
- [类型](associated-items.md#associated-types)
- [常量](associated-items.md#associated-constants)

r[items.traits.namespace]
trait 声明在其所在模块或块的[类型命名空间][type namespace]中定义一个 trait。

r[items.traits.associated-item-namespaces]
关联项作为该 trait 的成员定义在各自的命名空间中。关联类型定义在类型命名空间中。关联常量和关联函数定义在值命名空间中。

r[items.traits.self-param]
所有 trait 都定义一个隐式类型参数 `Self`，指“正在实现此接口的类型”。trait 也可以包含额外的类型参数。这些类型参数（包括 `Self`）可以[像往常一样][generics]被其他 trait 等约束。

r[items.traits.impls]
trait 通过单独的[实现][implementations]为具体类型实现。

r[items.traits.associated-item-decls]
trait 函数可以用分号替换函数体从而省略函数体。这表示实现必须定义该函数。若 trait 函数定义了函数体，则该定义作为任何未覆盖它的实现的默认实现。类似地，关联常量可以省略等号和表达式，以表示实现必须定义常量值。关联类型永远不能定义类型，类型只能在实现中指定。

```rust
// 带定义和不带定义的关联 trait 项示例。
trait Example {
    const CONST_NO_DEFAULT: i32;
    const CONST_WITH_DEFAULT: i32 = 99;
    type TypeNoDefault;
    fn method_without_default(&self);
    fn method_with_default(&self) {}
}
```

r[items.traits.const-fn]
trait 函数不允许是 [`const`]。

r[items.traits.bounds]
## Trait 约束

泛型项可以将其 trait 用作类型参数上的[约束][bounds]。

r[items.traits.generic]
## 泛型 trait

可以为 trait 指定类型参数以使其成为泛型。它们出现在 trait 名之后，使用与[泛型函数][generic functions]相同的语法。

```rust
trait Seq<T> {
    fn len(&self) -> u32;
    fn elt_at(&self, n: u32) -> T;
    fn iter<F>(&self, f: F) where F: Fn(T);
}
```

<a id="object-safety"></a>
r[items.traits.dyn-compatible]
## Dyn 兼容性

r[items.traits.dyn-compatible.intro]
dyn 兼容的 trait 可以成为 [trait 对象][trait object]的基 trait。若 trait 具有下列性质，则它是 *dyn 兼容*的：

r[items.traits.dyn-compatible.supertraits]
* 所有[超 trait][supertraits]也必须是 dyn 兼容的。

r[items.traits.dyn-compatible.sized]
* `Sized` 不得是[超 trait][supertraits]。换句话说，它不得要求 `Self: Sized`。

r[items.traits.dyn-compatible.associated-consts]
* 不得有任何关联常量。

r[items.traits.dyn-compatible.associated-types]
* 不得有任何带泛型的关联类型。

r[items.traits.dyn-compatible.associated-functions]
* 所有关联函数必须要么可从 trait 对象分发，要么被显式标为不可分发：
    * 可分发函数必须：
        * 没有任何类型参数（不过允许生命周期参数）。
        * 是一个除接收者类型外不使用 `Self` 的[方法][method]。
        * 具有下列类型之一的接收者：
            * `&Self`（即 `&self`）
            * `&mut Self`（即 `&mut self`）
            * [`Box<Self>`]
            * [`Rc<Self>`]
            * [`Arc<Self>`]
            * [`Pin<P>`]，其中 `P` 是上述类型之一
        * 没有不透明返回类型；也就是说，
            * 不是 `async fn`（它具有隐藏的 `Future` 类型）。
            * 没有返回位置的 `impl Trait` 类型（`fn example(&self) -> impl Trait`）。
        * 没有 `where Self: Sized` 约束（接收者类型为 `Self`（即 `self`）隐含这一点）。
        * 没有 C 可变参数（`_: ...`）。
    * 显式不可分发的函数要求：
        * 具有 `where Self: Sized` 约束（接收者类型为 `Self`（即 `self`）隐含这一点）。

r[items.traits.dyn-compatible.async-traits]
* [`AsyncFn`]、[`AsyncFnMut`] 和 [`AsyncFnOnce`] trait 不是 dyn 兼容的。

> **注意**
> 这一概念以前称为*对象安全*。

```rust
## use std::rc::Rc;
## use std::sync::Arc;
## use std::pin::Pin;
// dyn 兼容方法的例子。
trait TraitMethods {
    fn by_ref(self: &Self) {}
    fn by_ref_mut(self: &mut Self) {}
    fn by_box(self: Box<Self>) {}
    fn by_rc(self: Rc<Self>) {}
    fn by_arc(self: Arc<Self>) {}
    fn by_pin(self: Pin<&Self>) {}
    fn with_lifetime<'a>(self: &'a Self) {}
    fn nested_pin(self: Pin<Arc<Self>>) {}
}
## struct S;
## impl TraitMethods for S {}
## let t: Box<dyn TraitMethods> = Box::new(S);
```

```rust
// 此 trait 是 dyn 兼容的，但这些方法不能在 trait 对象上分发。
trait NonDispatchable {
    // 非方法不能被分发。
    fn foo() where Self: Sized {}
    // Self 类型直到运行时才知道。
    fn returns(&self) -> Self where Self: Sized;
    // `other` 可能是接收者的另一种具体类型。
    fn param(&self, other: Self) where Self: Sized {}
    // 泛型与 vtable 不兼容。
    fn typed<T>(&self, x: T) where Self: Sized {}
}

struct S;
impl NonDispatchable for S {
    fn returns(&self) -> Self where Self: Sized { S }
}
let obj: Box<dyn NonDispatchable> = Box::new(S);
obj.returns(); // 错误：不能用 Self 返回类型调用
obj.param(S);  // 错误：不能用 Self 参数调用
obj.typed(1);  // 错误：不能用泛型类型调用
```

```rust
## use std::rc::Rc;
// dyn 不兼容 trait 的例子。
trait DynIncompatible {
    const CONST: i32 = 1;  // 错误：不能有关联常量

    fn foo() {}  // 错误：没有 Sized 的关联函数
    fn returns(&self) -> Self; // 错误：返回类型中有 Self
    fn typed<T>(&self, x: T) {} // 错误：有泛型类型参数
    fn nested(self: Rc<Box<Self>>) {} // 错误：嵌套接收者不能被分发
}

struct S;
impl DynIncompatible for S {
    fn returns(&self) -> Self { S }
}
let obj: Box<dyn DynIncompatible> = Box::new(S); // 错误
```

```rust
// `Self: Sized` 的 trait 是 dyn 不兼容的。
trait TraitWithSize where Self: Sized {}

struct S;
impl TraitWithSize for S {}
let obj: Box<dyn TraitWithSize> = Box::new(S); // 错误
```

```rust
// 若 `Self` 是类型实参，则 dyn 不兼容。
trait Super<A> {}
trait WithSelf: Super<Self> where Self: Sized {}

struct S;
impl<A> Super<A> for S {}
impl WithSelf for S {}
let obj: Box<dyn WithSelf> = Box::new(S); // 错误：不能使用 `Self` 类型参数
```

r[items.traits.supertraits]
## 超 trait

r[items.traits.supertraits.intro]
**超 trait**（supertrait）是类型要实现某个特定 trait 时所必须实现的 trait。此外，任何被某个 trait 约束的[泛型][generics]或 [trait 对象][trait object]都可以访问其超 trait 的关联项。

r[items.traits.supertraits.decl]
超 trait 通过 trait 的 `Self` 类型上的 trait 约束声明，并传递地包含那些 trait 约束中所声明 trait 的超 trait。trait 成为其自身的超 trait 是错误的。

r[items.traits.supertraits.subtrait]
具有超 trait 的 trait 称为其超 trait 的 **子 trait**（subtrait）。

下面是一个将 `Shape` 声明为 `Circle` 的超 trait 的例子。

```rust
trait Shape { fn area(&self) -> f64; }
trait Circle: Shape { fn radius(&self) -> f64; }
```

下面是同一个例子，只不过使用了 [where 子句][where clauses]。

```rust
trait Shape { fn area(&self) -> f64; }
trait Circle where Self: Shape { fn radius(&self) -> f64; }
```

下一个例子使用来自 `Shape` 的 `area` 函数为 `radius` 给出默认实现。

```rust
## trait Shape { fn area(&self) -> f64; }
trait Circle where Self: Shape {
    fn radius(&self) -> f64 {
        // A = pi * r^2
        // 因此代数上，
        // r = sqrt(A / pi)
        (self.area() / std::f64::consts::PI).sqrt()
    }
}
```

下一个例子在泛型参数上调用超 trait 方法。

```rust
## trait Shape { fn area(&self) -> f64; }
## trait Circle: Shape { fn radius(&self) -> f64; }
fn print_area_and_radius<C: Circle>(c: C) {
    // 这里我们调用 `Circle` 的超 trait `Shape` 中的 area 方法。
    println!("Area: {}", c.area());
    println!("Radius: {}", c.radius());
}
```

类似地，这里是一个在 trait 对象上调用超 trait 方法的例子。

```rust
## trait Shape { fn area(&self) -> f64; }
## trait Circle: Shape { fn radius(&self) -> f64; }
## struct UnitCircle;
## impl Shape for UnitCircle { fn area(&self) -> f64 { std::f64::consts::PI } }
## impl Circle for UnitCircle { fn radius(&self) -> f64 { 1.0 } }
## let circle = UnitCircle;
let circle = Box::new(circle) as Box<dyn Circle>;
let nonsense = circle.radius() * circle.area();
```

r[items.traits.safety]
## 不安全 trait

r[items.traits.safety.intro]
以 `unsafe` 关键字开头的 trait 项表明*实现*该 trait 可能是[不安全][unsafe]的。使用正确实现的不安全 trait 是安全的。[trait 实现][trait implementation]也必须以 `unsafe` 关键字开头。

[`Sync`] 和 [`Send`] 是不安全 trait 的例子。

r[items.traits.params]
## 参数模式

r[items.traits.params.patterns-no-body]
没有函数体的关联函数中的参数只允许 [IDENTIFIER] 或 `_` [通配符][WildcardPattern]模式，以及 [SelfParam] 所允许的形式。目前允许 `mut` [IDENTIFIER]，但它已弃用，将来会成为硬错误。
<!-- https://github.com/rust-lang/rust/issues/35203 -->

```rust
trait T {
    fn f1(&self);
    fn f2(x: Self, _: i32);
}
```

```rust
trait T {
    fn f2(&x: &i32); // 错误：没有函数体的函数中不允许模式
}
```

r[items.traits.params.patterns-with-body]
有函数体的关联函数中的参数只允许不可反驳模式。

```rust
trait T {
    fn f1((a, b): (i32, i32)) {} // 可以：不可反驳
}
```

```rust
trait T {
    fn f1(123: i32) {} // 错误：模式可反驳
    fn f2(Some(x): Option<i32>) {} // 错误：模式可反驳
}
```

r[items.traits.params.pattern-required.edition2018]
> [!EDITION-2018]
> 在 2018 edition 之前，关联函数参数的模式是可选的：
>
> ```rust
> // 2015 Edition
> trait T {
>     fn f(i32); // 可以：不要求参数标识符
> }
> ```
>
> 从 2018 edition 开始，模式不再是可选的。

r[items.traits.params.restriction-patterns.edition2018]
> [!EDITION-2018]
> 在 2018 edition 之前，有函数体的关联函数中的参数仅限于下列种类的模式：
>
> * [IDENTIFIER]
> * `mut` [IDENTIFIER]
> * [`_`][WildcardPattern]
> * `&` [IDENTIFIER]
> * `&&` [IDENTIFIER]
>
> ```rust
> // 2015 Edition
> trait T {
>     fn f1((a, b): (i32, i32)) {} // 错误：不允许该模式
> }
> ```
>
> 从 2018 开始，如 [items.traits.params.patterns-with-body] 所述，允许所有不可反驳模式。

r[items.traits.associated-visibility]
## 项可见性

r[items.traits.associated-visibility.intro]
trait 项在语法上允许 [Visibility] 注解，但在验证 trait 时会被拒绝。这使项可以在不同使用上下文中以统一语法被解析。例如，可以为 trait 项使用空的 `vis` 宏片段说明符，而该宏规则还可以用在允许可见性的其他场合。

```rust
macro_rules! create_method {
    ($vis:vis $name:ident) => {
        $vis fn $name(&self) {}
    };
}

trait T1 {
    // 允许空的 `vis`。
    create_method! { method_of_t1 }
}

struct S;

impl S {
    // 这里允许可见性。
    create_method! { pub method_of_s }
}

impl T1 for S {}

fn main() {
    let s = S;
    s.method_of_t1();
    s.method_of_s();
}
```

[WildcardPattern]: ../patterns.md#wildcard-pattern
[bounds]: ../trait-bounds.md
[trait object]: ../types/trait-object.md
[associated items]: associated-items.md
[method]: associated-items.md#methods
[supertraits]: #supertraits
[implementations]: implementations.md
[generics]: generics.md
[where clauses]: generics.md#where-clauses
[generic functions]: functions.md#generic-functions
[unsafe]: ../unsafety.md
[trait implementation]: implementations.md#trait-implementations
[`Send`]: ../special-types-and-traits.md#send
[`Sync`]: ../special-types-and-traits.md#sync
[`Arc<Self>`]: ../special-types-and-traits.md#arct
[`Box<Self>`]: ../special-types-and-traits.md#boxt
[`Pin<P>`]: ../special-types-and-traits.md#pinp
[`Rc<Self>`]: ../special-types-and-traits.md#rct
[`async`]: functions.md#async-functions
[`const`]: functions.md#const-functions
[type namespace]: ../names/namespaces.md
