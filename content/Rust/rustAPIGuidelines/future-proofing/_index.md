+++
title = "第10章 面向未来"
date = 2026-08-18T21:50:00+08:00
weight = 120
type = "docs"
description = "面向未来 — Rust API Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

> 原文链接: [https://rust-lang.github.io/api-guidelines/future-proofing.html](https://rust-lang.github.io/api-guidelines/future-proofing.html)

# 面向未来

## 密封 trait 防止下游实现 (C-SEALED) {#c-sealed}

有些 trait 只打算在定义它们的 crate 内部实现。在这种情况下，通过使用密封 trait 模式，我们可以保留以非破坏性方式修改该 trait 的能力。

```rust
/// 该 trait 已密封，crate 外部的类型无法实现它。
pub trait TheTrait: private::Sealed {
    // 零个或多个允许用户调用的方法。
    fn ...();

    // 零个或多个私有方法，不允许用户调用。
    #[doc(hidden)]
    fn ...();
}

// 为某些类型实现。
impl TheTrait for usize {
    /* ... */
}

mod private {
    pub trait Sealed {}

    // 为上述同样的类型实现，但不为其他类型实现。
    impl Sealed for usize {}
}
```

这个空的私有 `Sealed` 超 trait 无法被下游 crate 命名，因此可以保证 `Sealed`（进而 `TheTrait`）的实现只存在于当前 crate。我们可以在非破坏性发布中向 `TheTrait` 添加方法，尽管对于未密封的 trait 这通常会是破坏性变更。此外，我们也可以自由更改未公开文档化的方法的签名。

注意，移除密封 trait 中的公有方法，或更改公有方法的签名，仍然是破坏性变更。

为了避免用户徒劳地尝试实现该 trait，应当在 rustdoc 中说明该 trait 是密封的，且不打算在当前 crate 之外实现。

### 示例

- [`serde_json::value::Index`](https://docs.serde.rs/serde_json/value/trait.Index.html)
- [`byteorder::ByteOrder`](https://docs.rs/byteorder/1.1.0/byteorder/trait.ByteOrder.html)

## 结构体字段为私有 (C-STRUCT-PRIVATE) {#c-struct-private}

将字段设为公有是一项很强的承诺：它固定了一种表示选择，*并且*使该类型无法对字段内容提供任何校验或维持任何不变量，因为客户端可以任意修改它。

公有字段最适合带有 C 风格精神的 `struct` 类型：复合的、被动的数据结构。否则，考虑提供 getter/setter 方法并隐藏字段。

## Newtype 封装实现细节 (C-NEWTYPE-HIDE) {#c-newtype-hide}

Newtype 可用于隐藏表示细节，同时向客户端做出精确承诺。

例如，考虑一个返回复合迭代器类型的函数 `my_transform`。

```rust
use std::iter::{Enumerate, Skip};

pub fn my_transform<I: Iterator>(input: I) -> Enumerate<Skip<I>> {
    input.skip(3).enumerate()
}
```

我们希望对客户端隐藏该类型，使客户端看到的返回类型大致是 `Iterator<Item = (usize, T)>`。可以用 newtype 模式做到这一点：

```rust
use std::iter::{Enumerate, Skip};

pub struct MyTransformResult<I>(Enumerate<Skip<I>>);

impl<I: Iterator> Iterator for MyTransformResult<I> {
    type Item = (usize, I::Item);

    fn next(&mut self) -> Option<Self::Item> {
        self.0.next()
    }
}

pub fn my_transform<I: Iterator>(input: I) -> MyTransformResult<I> {
    MyTransformResult(input.skip(3).enumerate())
}
```

除了简化签名之外，这种 newtype 用法还让我们对客户端承诺得更少。客户端不知道结果迭代器是*如何*构造或表示的，这意味着将来可以改变表示而不破坏客户端代码。

Rust 1.26 还引入了 [`impl Trait`][] 特性，它比 newtype 模式更简洁，但有一些额外权衡，即使用 `impl Trait` 时你能表达的内容有限。例如，返回一个实现了 `Debug` 或 `Clone`，或其他迭代器扩展 trait 某种组合的迭代器，可能会有问题。总之，将 `impl Trait` 作为返回类型对内部 API 大概很好，甚至也可能适合公有 API，但大概并非所有情况都适合。更多细节见版本指南（Edition Guide）中 [「用 `impl Trait` 轻松返回复杂类型」][impl-trait-2] 一节。

[`impl Trait`]: https://github.com/rust-lang/rfcs/blob/master/text/1522-conservative-impl-trait.md
[impl-trait-2]: https://rust-lang.github.io/edition-guide/rust-2018/trait-system/impl-trait-for-returning-complex-types-with-ease.html

```rust
pub fn my_transform<I: Iterator>(input: I) -> impl Iterator<Item = (usize, I::Item)> {
    input.skip(3).enumerate()
}
```

## 数据结构不重复派生 trait 约束 (C-STRUCT-BOUNDS) {#c-struct-bounds}

泛型数据结构不应使用可以派生、或不另外增加语义价值的 trait 约束。`derive` 属性中的每个 trait 都会展开为单独的 `impl` 块，且仅适用于实现了该 trait 的泛型参数。

```rust
// 优先这样写：
#[derive(Clone, Debug, PartialEq)]
struct Good<T> { /* ... */ }

// 而不是这样：
#[derive(Clone, Debug, PartialEq)]
struct Bad<T: Clone + Debug + PartialEq> { /* ... */ }
```

在 `Bad` 上把已派生的 trait 再重复为约束是不必要的，而且是向后兼容性隐患。为说明这一点，考虑在上一示例的结构体上派生 `PartialOrd`：

```rust
// 非破坏性变更：
#[derive(Clone, Debug, PartialEq, PartialOrd)]
struct Good<T> { /* ... */ }

// 破坏性变更：
#[derive(Clone, Debug, PartialEq, PartialOrd)]
struct Bad<T: Clone + Debug + PartialEq + PartialOrd> { /* ... */ }
```

一般而言，向数据结构添加 trait 约束是破坏性变更，因为该结构的每个使用者都需要开始满足额外约束。使用 `derive` 属性从标准库派生更多 trait 不是破坏性变更。

以下 trait 绝不应当用在数据结构的约束中：

- `Clone`
- `PartialEq`
- `PartialOrd`
- `Debug`
- `Display`
- `Default`
- `Error`
- `Serialize`
- `Deserialize`
- `DeserializeOwned`

其他并非结构体定义所严格需要的、不可派生的 trait 约束（如 `Read` 或 `Write`）存在灰色地带。它们可能在定义中更好地传达该类型的预期行为，但也会限制未来的可扩展性。在数据结构上包含有语义价值的 trait 约束，仍然比把可派生 trait 作为约束问题更小。

### 例外

在结构体上需要 trait 约束的情况有三个例外：

1. 数据结构引用了该 trait 上的关联类型。
1. 约束是 `?Sized`。
1. 数据结构有一个需要 trait 约束的 `Drop` 实现。
Rust 当前要求 `Drop` 实现上的所有 trait 约束也出现在数据结构上。

### 标准库中的示例

- [`std::borrow::Cow`] 引用了 `Borrow` trait 上的关联类型。
- [`std::boxed::Box`] 选择退出了隐式的 `Sized` 约束。
- [`std::io::BufWriter`] 在其 `Drop` 实现中需要 trait 约束。

[`std::borrow::Cow`]: https://doc.rust-lang.org/std/borrow/enum.Cow.html
[`std::boxed::Box`]: https://doc.rust-lang.org/std/boxed/struct.Box.html
[`std::io::BufWriter`]: https://doc.rust-lang.org/std/io/struct.BufWriter.html
