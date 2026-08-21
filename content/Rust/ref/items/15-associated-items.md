+++
title = "15-关联项"
date = 2026-08-18T08:45:00+08:00
weight = 32
type = "docs"
description = "关联项 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/items/associated-items.html](https://doc.rust-lang.org/reference/items/associated-items.html)

r[items.associated]
# 关联项

r[items.associated.syntax]
```grammar,items
AssociatedItem ->
    OuterAttribute* (
        MacroInvocationSemi
      | ( Visibility? ( TypeAlias | ConstantItem | Function ) )
    )
```

r[items.associated.intro]
*关联项*是在 [trait][traits] 中声明或在[实现][implementations]中定义的项。之所以这样称呼，是因为它们定义在关联类型上——即实现中的类型。

r[items.associated.kinds]
它们是可以在模块中声明的项种类的子集。具体来说，有[关联函数][associated functions]（包括方法）、[关联类型][associated types]和[关联常量][associated constants]。

[associated functions]: #associated-functions-and-methods
[associated types]: #associated-types
[associated constants]: #associated-constants

r[items.associated.related]
当关联项在逻辑上与进行关联的项相关时，关联项很有用。例如，`Option` 上的 `is_some` 方法本质上与 Option 相关，因此应当是关联的。

r[items.associated.decl-def]
每种关联项都有两种形式：包含实际实现的定义，以及为定义声明签名的声明。

r[items.associated.trait-items]
构成 trait 契约以及泛型类型上可用内容的，正是这些声明。

r[items.associated.fn]
## 关联函数与方法

r[items.associated.fn.intro]
*关联函数*是与类型关联的[函数][functions]。

r[items.associated.fn.decl]
*关联函数声明*为关联函数定义声明签名。它写成函数项，只不过函数体被替换为 `;`。

r[items.associated.name]
该标识符是函数的名称。

r[items.associated.same-signature]
关联函数的泛型、参数列表、返回类型和 where 子句必须与关联函数声明的相同。

r[items.associated.fn.def]
*关联函数定义*定义与另一类型关联的函数。其写法与[函数项][function item]相同。

> **注意**
> 一个常见例子是名为 `new` 的关联函数，它返回与之关联的类型的值。

```rust
struct Struct {
    field: i32
}

impl Struct {
    fn new() -> Struct {
        Struct {
            field: 0i32
        }
    }
}

fn main () {
    let _struct = Struct::new();
}
```

r[items.associated.fn.qualified-self]
当关联函数在 trait 上声明时，也可以用一条路径来调用该函数，该路径是到该 trait 的路径后接该函数的名称。发生这种情况时，它会被替换为 `<_ as Trait>::function_name`。

```rust
trait Num {
    fn from_i32(n: i32) -> Self;
}

impl Num for f64 {
    fn from_i32(n: i32) -> f64 { n as f64 }
}

// 在此情况下这 4 个是等价的。
let _: f64 = Num::from_i32(42);
let _: f64 = <_ as Num>::from_i32(42);
let _: f64 = <f64 as Num>::from_i32(42);
let _: f64 = f64::from_i32(42);
```

r[items.associated.fn.method]
### 方法

r[items.associated.fn.method.intro]
第一个参数名为 `self` 的关联函数称为*方法*，可以使用[方法调用运算符][method call operator]调用，例如 `x.foo()`，也可以使用通常的函数调用记法。

r[items.associated.fn.method.self-ty]
若指定了 `self` 参数的类型，则它仅限于解析为由下列语法生成的类型（其中 `'lt` 表示某个任意生命周期）：

```text
P = &'lt S | &'lt mut S | Box<S> | Rc<S> | Arc<S> | Pin<P>
S = Self | P
```

此语法中的 `Self` 终结符表示解析为实现类型的类型。这也可以包括上下文类型别名 `Self`、其他类型别名，或解析为实现类型的关联类型投影。

```rust
## use std::rc::Rc;
## use std::sync::Arc;
## use std::pin::Pin;
// 在结构体 `Example` 上实现的方法的例子。
struct Example;
type Alias = Example;
trait Trait { type Output; }
impl Trait for Example { type Output = Example; }
impl Example {
    fn by_value(self: Self) {}
    fn by_ref(self: &Self) {}
    fn by_ref_mut(self: &mut Self) {}
    fn by_box(self: Box<Self>) {}
    fn by_rc(self: Rc<Self>) {}
    fn by_arc(self: Arc<Self>) {}
    fn by_pin(self: Pin<&Self>) {}
    fn explicit_type(self: Arc<Example>) {}
    fn with_lifetime<'a>(self: &'a Self) {}
    fn nested<'a>(self: &mut &'a Arc<Rc<Box<Alias>>>) {}
    fn via_projection(self: <Example as Trait>::Output) {}
}
```

r[associated.fn.method.self-pat-shorthands]
可以使用不指定类型的简写语法，它们有下列等价形式：

简写                  | 等价形式
----------------------|-----------
`self`                | `self: Self`
`&'lifetime self`     | `self: &'lifetime Self`
`&'lifetime mut self` | `self: &'lifetime mut Self`

> **注意**
> 使用此简写时，生命周期可以、而且通常会被省略。

r[associated.fn.method.self-pat-mut]
若 `self` 参数以 `mut` 为前缀，则它变成可变变量，类似于使用 `mut` [标识符模式][identifier pattern]的普通参数。例如：

```rust
trait Changer: Sized {
    fn change(mut self) {}
    fn modify(mut self: Box<Self>) {}
}
```

作为 trait 上方法的例子，考虑下列代码：

```rust
## type Surface = i32;
## type BoundingBox = i32;
trait Shape {
    fn draw(&self, surface: Surface);
    fn bounding_box(&self) -> BoundingBox;
}
```

这定义了一个带有两个方法的 trait。所有实现了此 trait 且该 trait 处于作用域中的值，都可以调用它们的 `draw` 和 `bounding_box` 方法。

```rust
## type Surface = i32;
## type BoundingBox = i32;
## trait Shape {
##     fn draw(&self, surface: Surface);
##     fn bounding_box(&self) -> BoundingBox;
## }
#
struct Circle {
    // ...
}

impl Shape for Circle {
    // ...
##   fn draw(&self, _: Surface) {}
##   fn bounding_box(&self) -> BoundingBox { 0i32 }
}

## impl Circle {
##     fn new() -> Circle { Circle{} }
## }
#
let circle_shape = Circle::new();
let bounding_box = circle_shape.bounding_box();
```

r[items.associated.fn.params.edition2018]
> [!EDITION-2018]
> 在 2015 edition 中，可以声明带有匿名参数的 trait 方法（例如 `fn foo(u8)`）。这已弃用，并且从 2018 edition 起是错误。所有参数都必须有实参名。

r[items.associated.fn.param-attributes]
#### 方法参数上的属性

方法参数上的属性遵循与[普通函数参数][regular function parameters]相同的规则和限制。

r[items.associated.type]
## 关联类型

r[items.associated.type.intro]
*关联类型*是与另一类型关联的[类型别名][type aliases]。

r[items.associated.type.restrictions]
关联类型不能在[固有实现][inherent implementations]中定义，也不能在 trait 中给出默认实现。

r[items.associated.type.decl]
*关联类型声明*为关联类型定义声明签名。它写成下列形式之一，其中 `Assoc` 是关联类型的名称，`Params` 是类型、生命周期或常量参数的逗号分隔列表，`Bounds` 是关联类型必须满足的 trait 约束的加号分隔列表，`WhereBounds` 是参数必须满足的约束的逗号分隔列表：

<!-- ignore: illustrative example forms -->
```rust
type Assoc;
type Assoc: Bounds;
type Assoc<Params>;
type Assoc<Params>: Bounds;
type Assoc<Params> where WhereBounds;
type Assoc<Params>: Bounds where WhereBounds;
```

r[items.associated.type.name]
该标识符是所声明类型别名的名称。

r[items.associated.type.impl-fulfillment]
可选的 trait 约束必须由该类型别名的实现满足。

r[items.associated.type.sized]
关联类型上有隐式的 [`Sized`] 约束，可以使用特殊的 `?Sized` 约束放宽。

r[items.associated.type.def]
*关联类型定义*为在某类型上实现 trait 定义类型别名。

r[items.associated.type.def.restriction]
它们的写法类似于*关联类型声明*，但不能包含 `Bounds`，而必须包含 `Type`：

<!-- ignore: illustrative example forms -->
```rust
type Assoc = Type;
type Assoc<Params> = Type; // 这里的类型 `Type` 可以引用 `Params`
type Assoc<Params> = Type where WhereBounds;
type Assoc<Params> where WhereBounds = Type; // 已弃用，更推荐上面的形式
```

r[items.associated.type.alias]
若类型 `Item` 具有来自 trait `Trait` 的关联类型 `Assoc`，则 `<Item as Trait>::Assoc` 是作为关联类型定义中所指定类型之别名的类型。

r[items.associated.type.param]
此外，若 `Item` 是类型参数，则 `Item::Assoc` 可以用在类型参数中。

r[items.associated.type.generic]
关联类型可以包含[泛型参数][generic parameters]和 [where 子句][where clauses]；这些通常称为*泛型关联类型*，或 *GAT*。若类型 `Thing` 具有来自带泛型 `<'a>` 的 trait `Trait` 的关联类型 `Item`，则该类型可以命名为 `<Thing as Trait>::Item<'x>`，其中 `'x` 是作用域中的某个生命周期。在此情况下，`'x` 会用在 impl 上的关联类型定义中 `'a` 出现的任何地方。

```rust
trait AssociatedType {
    // 关联类型声明
    type Assoc;
}

struct Struct;

struct OtherStruct;

impl AssociatedType for Struct {
    // 关联类型定义
    type Assoc = OtherStruct;
}

impl OtherStruct {
    fn new() -> OtherStruct {
        OtherStruct
    }
}

fn main() {
    // 使用关联类型将 OtherStruct 指称为 <Struct as AssociatedType>::Assoc
    let _other_struct: OtherStruct = <Struct as AssociatedType>::Assoc::new();
}
```

带有泛型和 where 子句的关联类型的例子：

```rust
struct ArrayLender<'a, T>(&'a mut [T; 16]);

trait Lend {
    // 泛型关联类型声明
    type Lender<'a> where Self: 'a;
    fn lend<'a>(&'a mut self) -> Self::Lender<'a>;
}

impl<T> Lend for [T; 16] {
    // 泛型关联类型定义
    type Lender<'a> = ArrayLender<'a, T> where Self: 'a;

    fn lend<'a>(&'a mut self) -> Self::Lender<'a> {
        ArrayLender(self)
    }
}

fn borrow<'a, T: Lend>(array: &'a mut T) -> <T as Lend>::Lender<'a> {
    array.lend()
}

fn main() {
    let mut array = [0usize; 16];
    let lender = borrow(&mut array);
}
```

### 关联类型容器示例

考虑下列 `Container` trait 的例子。注意该类型可以在方法签名中使用：

```rust
trait Container {
    type E;
    fn empty() -> Self;
    fn insert(&mut self, elem: Self::E);
}
```

类型要实现此 trait，不仅必须为每个方法提供实现，还必须指定类型 `E`。下面是标准库类型 `Vec` 对 `Container` 的实现：

```rust
## trait Container {
##     type E;
##     fn empty() -> Self;
##     fn insert(&mut self, elem: Self::E);
## }
impl<T> Container for Vec<T> {
    type E = T;
    fn empty() -> Vec<T> { Vec::new() }
    fn insert(&mut self, x: T) { self.push(x); }
}
```

### `Bounds` 与 `WhereBounds` 的关系

在此例中：

```rust
## use std::fmt::Debug;
trait Example {
    type Output<T>: Ord where T: Debug;
}
```

给定对关联类型的引用如 `<X as Example>::Output<Y>`，关联类型本身必须是 `Ord`，并且类型 `Y` 必须是 `Debug`。

r[items.associated.type.generic-where-clause]
### 泛型关联类型上必需的 where 子句

r[items.associated.type.generic-where-clause.intro]
trait 上的泛型关联类型声明目前可能需要一组 where 子句，取决于 trait 中的函数以及 GAT 的使用方式。这些规则将来可能会放宽；更新可以在[泛型关联类型倡议仓库](https://rust-lang.github.io/generic-associated-types-initiative/explainer/required_bounds.html)中找到。

r[items.associated.type.generic-where-clause.valid-fn]
简而言之，要求这些 where 子句是为了最大化 impl 中关联类型所允许的定义。为此，在 GAT 作为输入或输出出现的函数上（使用该函数或 trait 的参数）*可以证明成立*的任何子句，也必须写在 GAT 本身上。

```rust
trait LendingIterator {
    type Item<'x> where Self: 'x;
    fn next<'a>(&'a mut self) -> Self::Item<'a>;
}
```

在上面，对于 `next` 函数，我们可以证明 `Self: 'a`，因为来自 `&'a mut self` 的隐含约束；因此，我们必须在 GAT 本身上写上等价的约束：`where Self: 'x`。

r[items.associated.type.generic-where-clause.intersection]
当 trait 中有多个函数使用该 GAT 时，使用的是来自不同函数的约束的*交集*，而不是并集。

```rust
trait Check<T> {
    type Checker<'x>;
    fn create_checker<'a>(item: &'a T) -> Self::Checker<'a>;
    fn do_check(checker: Self::Checker<'_>);
}
```

在此例中，`type Checker<'a>;` 上不需要约束。虽然我们知道在 `create_checker` 上有 `T: 'a`，但在 `do_check` 上并不知道。不过，若注释掉 `do_check`，则 `Checker` 上会需要 `where T: 'x` 约束。

r[items.associated.type.generic-where-clause.forward]
关联类型上的约束也会传播必需的 where 子句。

```rust
trait Iterable {
    type Item<'a> where Self: 'a;
    type Iterator<'a>: Iterator<Item = Self::Item<'a>> where Self: 'a;
    fn iter<'a>(&'a self) -> Self::Iterator<'a>;
}
```

这里，由于 `iter`，`Item` 上需要 `where Self: 'a`。然而，`Item` 用在 `Iterator` 的约束中，因此那里也需要 `where Self: 'a` 子句。

r[items.associated.type.generic-where-clause.static]
最后，trait 中 GAT 上对 `'static` 的任何显式使用都不计入必需约束。

```rust
trait StaticReturn {
    type Y<'a>;
    fn foo(&self) -> Self::Y<'static>;
}
```

r[items.associated.const]
## 关联常量

r[items.associated.const.intro]
*关联常量*是与类型关联的[常量][constants]。

r[items.associated.const.decl]
*关联常量声明*为关联常量定义声明签名。它写成 `const`，然后是标识符，然后是 `:`，然后是类型，以 `;` 结束。

r[items.associated.const.name]
该标识符是路径中使用的常量名称。该类型是定义必须实现的类型。

r[items.associated.const.def]
*关联常量定义*定义与类型关联的常量。其写法与[常量项][constant item]相同。

r[items.associated.const.eval]
关联常量定义仅在被引用时才进行[常量求值][constant evaluation]。此外，包含[泛型参数][generic parameters]的定义在单态化之后求值。

```rust
struct Struct;
struct GenericStruct<const ID: i32>;

impl Struct {
    // 定义不会立即求值
    const PANIC: () = panic!("compile-time panic");
}

impl<const ID: i32> GenericStruct<ID> {
    // 定义不会立即求值
    const NON_ZERO: () = if ID == 0 {
        panic!("contradiction")
    };
}

fn main() {
    // 引用 Struct::PANIC 会导致编译错误
    let _ = Struct::PANIC;

    // 可以，ID 不是 0
    let _ = GenericStruct::<1>::NON_ZERO;

    // 以 ID=0 求值 NON_ZERO 导致编译错误
    let _ = GenericStruct::<0>::NON_ZERO;
}
```

### 关联常量示例

一个基本例子：

```rust
trait ConstantId {
    const ID: i32;
}

struct Struct;

impl ConstantId for Struct {
    const ID: i32 = 1;
}

fn main() {
    assert_eq!(1, Struct::ID);
}
```

使用默认值：

```rust
trait ConstantIdDefault {
    const ID: i32 = 1;
}

struct Struct;
struct OtherStruct;

impl ConstantIdDefault for Struct {}

impl ConstantIdDefault for OtherStruct {
    const ID: i32 = 5;
}

fn main() {
    assert_eq!(1, Struct::ID);
    assert_eq!(5, OtherStruct::ID);
}
```

[`Arc<Self>`]: ../special-types-and-traits.md#arct
[`Box<Self>`]: ../special-types-and-traits.md#boxt
[`Pin<P>`]: ../special-types-and-traits.md#pinp
[`Rc<Self>`]: ../special-types-and-traits.md#rct
[`Sized`]: ../special-types-and-traits.md#sized
[traits]: traits.md
[type aliases]: type-aliases.md
[inherent implementations]: implementations.md#inherent-implementations
[identifier]: ../identifiers.md
[identifier pattern]: ../patterns.md#identifier-patterns
[implementations]: implementations.md
[type]: ../types.md#type-expressions
[constants]: constant-items.md
[constant item]: constant-items.md
[functions]: functions.md
[function item]: ../types/function-item.md
[method call operator]: ../expressions/method-call-expr.md
[path]: ../paths.md
[regular function parameters]: functions.md#attributes-on-function-parameters
[generic parameters]: generics.md
[where clauses]: generics.md#where-clauses
[constant evaluation]: ../const_eval.md
