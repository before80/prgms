+++
title = "第11章 特殊类型与 Trait"
date = 2026-08-18T08:45:00+08:00
weight = 94
type = "docs"
description = "特殊类型与 Trait — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/special-types-and-traits.html](https://doc.rust-lang.org/reference/special-types-and-traits.html)

r[lang-types]
# 特殊类型与 Trait

r[lang-types.intro]
[标准库][the standard library]中的某些类型与 trait 为 Rust 编译器所知。本章记录这些类型与 trait 的特殊功能。

r[lang-types.box]
## `Box<T>`

r[lang-types.box.intro]
[`Box<T>`] 具有若干目前不允许用户自定义类型拥有的特殊功能。

r[lang-types.box.deref]
* `Box<T>` 的[解引用运算符][dereference operator]产生一个可以[移出][moved from]的场所。这意味着 `*` 运算符以及 `Box<T>` 的析构器是语言内建的。

r[lang-types.box.receiver]
* [方法][Methods]可以将 `Box<Self>` 作为接收者。

r[lang-types.box.fundamental]
* 可以在与 `T` 相同的 crate 中为 `Box<T>` 实现 trait，而[孤儿规则][orphan rules]对其他泛型类型会禁止这种做法。

<!-- Editor Note: This is nowhere close to an exhaustive list -->

r[lang-types.rc]
## `Rc<T>`

r[lang-types.rc.receiver]
[方法][Methods]可以将 [`Rc<Self>`] 作为接收者。

r[lang-types.arc]
## `Arc<T>`

r[lang-types.arc.receiver]
[方法][Methods]可以将 [`Arc<Self>`] 作为接收者。

r[lang-types.pin]
## `Pin<P>`

r[lang-types.pin.receiver]
[方法][Methods]可以将 [`Pin<P>`] 作为接收者。

r[lang-types.unsafe-cell]
## `UnsafeCell<T>`

r[lang-types.unsafe-cell.interior-mut]
[`std::cell::UnsafeCell<T>`] 用于[内部可变性][interior mutability]。它确保编译器不会对此类类型执行不正确的优化。

r[lang-types.unsafe-cell.read-only-alloc]
它还确保类型具有内部可变性的 [`static` 项][`static` items] 不会被放入标记为只读的内存中。

r[lang-types.phantom-data]
## `PhantomData<T>`

[`std::marker::PhantomData<T>`] 是一种[零大小][zero-sized]、最小对齐的类型；就[变性][variance]、[析构检查][drop check]以及[自动 trait](#auto-traits)而言，它被视为拥有一个 `T`。

r[lang-types.va-list]
## `VaList<'_>`

[`VaList`] 用于 [C 可变参数函数][C-variadic functions]。

> **注意**
> [`VaList`] 在 ABI 上与 C 的 `va_list` 类型兼容；参见 [items.fn.c-variadic.abi-compatibility]。

r[lang-types.ops]
## 运算符 trait

[`std::ops`] 与 [`std::cmp`] 中的 trait 用于重载[运算符][operators]、[索引表达式][indexing expressions]以及[调用表达式][call expressions]。

r[lang-types.deref]
## `Deref` 与 `DerefMut`

除了重载一元 `*` 运算符外，[`Deref`] 与 [`DerefMut`] 还用于[方法解析][method resolution]以及[解引用强制转换][deref coercions]。

r[lang-types.drop]
## `Drop`

[`Drop`] trait 提供[析构器][destructor]，在该类型的值将被销毁时运行。

r[lang-types.copy]
## `Copy`

r[lang-types.copy.intro]
[`Copy`] trait 会改变实现它的类型的语义。

r[lang-types.copy.behavior]
实现了 `Copy` 的类型的值在赋值时会被复制，而不是移动。

r[lang-types.copy.constraint]
`Copy` 只能为未实现 `Drop`、且其所有字段都是 `Copy` 的类型实现。对枚举而言，这意味着所有变体的所有字段都必须是 `Copy`。对联合体而言，这意味着所有变体都必须是 `Copy`。

r[lang-types.copy.builtin-types]
编译器会为以下类型实现 `Copy`：

r[lang-types.copy.tuple]
* 由 `Copy` 类型组成的[元组][Tuples]

r[lang-types.copy.fn-pointer]
* [函数指针][Function pointers]

r[lang-types.copy.fn-item]
* [函数项][Function items]

r[lang-types.copy.closure]
* 未捕获任何值、或仅捕获 `Copy` 类型值的[闭包][Closures]

r[lang-types.clone]
## `Clone`

r[lang-types.clone.intro]
[`Clone`] trait 是 `Copy` 的超 trait，因此也需要由编译器生成实现。

r[lang-types.clone.builtin-types]
编译器为以下类型实现它：

r[lang-types.clone.builtin-copy]
* 具有内建 `Copy` 实现的类型（见上文）

r[lang-types.clone.tuple]
* 由 `Clone` 类型组成的[元组][Tuples]

r[lang-types.clone.closure]
* 仅捕获 `Clone` 类型值、或未从环境捕获任何值的[闭包][Closures]

r[lang-types.send]
## `Send`

[`Send`] trait 表示该类型的值可以安全地从一个线程发送到另一个线程。

r[lang-types.sync]
## `Sync`

r[lang-types.sync.intro]
[`Sync`] trait 表示该类型的值可以安全地在多个线程之间共享。

r[lang-types.sync.static-constraint]
用于不可变 [`static` 项][`static` items] 的所有类型都必须实现此 trait。

r[lang-types.termination]
## `Termination`

[`Termination`] trait 表示 [main 函数][main function]与[测试函数][test functions]可接受的返回类型。

r[lang-types.auto-traits]
## 自动 trait

[`Send`]、[`Sync`]、[`Unpin`]、[`UnwindSafe`] 与 [`RefUnwindSafe`] trait 是*自动 trait*。自动 trait 具有特殊性质。

r[lang-types.auto-traits.auto-impl]
若未为给定类型写出自动 trait 的显式实现或否定实现，则编译器会按下列规则自动实现它：

r[lang-types.auto-traits.builtin-composite]
* 若 `T` 实现该 trait，则 `&T`、`&mut T`、`*const T`、`*mut T`、`[T; n]` 与 `[T]` 也实现该 trait。

r[lang-types.auto-traits.fn-item-pointer]
* 函数项类型与函数指针自动实现该 trait。

r[lang-types.auto-traits.aggregate]
* 若结构体、枚举、联合体与元组的所有字段都实现该 trait，则它们也实现该 trait。

r[lang-types.auto-traits.closure]
* 若闭包所捕获的所有类型都实现该 trait，则闭包也实现该 trait。以共享引用捕获 `T`、以值捕获 `U` 的闭包，会实现 `&T` 与 `U` 都实现的那些自动 trait。

r[lang-types.auto-traits.generic-impl]
对于泛型类型（将上述内建类型视为关于 `T` 的泛型），若已有泛型实现可用，则对于本可使用该实现、但因不满足所需 trait 约束而无法使用的类型，编译器不会自动实现。例如，标准库为所有 `T: Sync` 的 `&T` 实现了 `Send`；这意味着若 `T` 是 `Send` 但不是 `Sync`，编译器不会为 `&T` 实现 `Send`。

r[lang-types.auto-traits.negative]
自动 trait 也可以有否定实现，在标准库文档中写作 `impl !AutoTrait for T`，用于覆盖自动实现。例如 `*mut T` 有 `Send` 的否定实现，因此即便 `T` 是 `Send`，`*mut T` 也不是 `Send`。目前尚无稳定方式指定额外的否定实现；它们仅存在于标准库中。

r[lang-types.auto-traits.trait-object-marker]
自动 trait 可以作为额外约束添加到任何[trait 对象][trait object]上，即便通常只允许一个 trait。例如，`Box<dyn Debug + Send + UnwindSafe>` 是有效类型。

r[lang-types.sized]
## `Sized`

r[lang-types.sized.intro]
[`Sized`] trait 表示该类型的大小在编译时已知；也就是说，它不是[动态大小类型][dynamically sized type]。

r[lang-types.sized.implicit-sized]
[类型参数][Type parameters]（trait 中的 `Self` 除外）默认是 `Sized` 的，[关联类型][associated types]亦然。

r[lang-types.sized.implicit-impl]
`Sized` 始终由编译器自动实现，而非由[实现项][implementation items]实现。

r[lang-types.sized.relaxation]
这些隐式的 `Sized` 约束可通过使用特殊的 `?Sized` 约束来放宽。

[`Arc<Self>`]: std::sync::Arc
[`Deref`]: std::ops::Deref
[`DerefMut`]: std::ops::DerefMut
[`Pin<P>`]: std::pin::Pin
[`Rc<Self>`]: std::rc::Rc
[`RefUnwindSafe`]: std::panic::RefUnwindSafe
[`Termination`]: std::process::Termination
[`UnwindSafe`]: std::panic::UnwindSafe
[`Unpin`]: std::marker::Unpin

[Arrays]: types/array.md
[associated types]: items/associated-items.md#associated-types
[call expressions]: expressions/call-expr.md
[C-variadic functions]: items.fn.c-variadic
[deref coercions]: type-coercions.md#coercion-types
[dereference operator]: expressions/operator-expr.md#the-dereference-operator
[destructor]: destructors.md
[drop check]: ../nomicon/dropck.html
[dynamically sized type]: dynamically-sized-types.md
[Function pointers]: types/function-pointer.md
[Function items]: types/function-item.md
[implementation items]: items/implementations.md
[indexing expressions]: expressions/array-expr.md#array-and-slice-indexing-expressions
[interior mutability]: interior-mutability.md
[main function]: crates-and-source-files.md#main-functions
[Methods]: items/associated-items.md#associated-functions-and-methods
[method resolution]: expressions/method-call-expr.md
[moved from]: expr.move.movable-place
[operators]: expressions/operator-expr.md
[orphan rules]: items/implementations.md#trait-implementation-coherence
[`static` items]: items/static-items.md
[test functions]: attributes/testing.md#the-test-attribute
[the standard library]: std
[trait object]: types/trait-object.md
[Tuples]: types/tuple.md
[Type parameters]: types/parameters.md
[`VaList`]: core::ffi::VaList
[variance]: subtyping.md#variance
[zero-sized]: glossary.zst
[Closures]: types/closure.md
