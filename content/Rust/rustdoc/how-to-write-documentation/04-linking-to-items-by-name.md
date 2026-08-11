+++
title = "04-按名称链接到项"
date = 2026-08-01T07:35:00+08:00
weight = 44
type = "docs"
description = "在文档中按名称链接到其他项"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The rustdoc book](https://doc.rust-lang.org/rustdoc/)

# 按名称链接到项 {#linking-to-items-by-name}


> 原文链接: [https://doc.rust-lang.org/rustdoc/write-documentation/linking-to-items-by-name.html](https://doc.rust-lang.org/rustdoc/write-documentation/linking-to-items-by-name.html)


Rustdoc 能够用项的路径作为链接，直接链接到其他 rustdoc 页面。这称为「文档内链接（intra-doc link）」。

例如，在下面的代码中，所有链接都会指向 `Bar` 的 rustdoc 页面：

```rust
/// 这个结构体不是 [Bar]
pub struct Foo1;

/// 这个结构体也不是 [bar](Bar)
pub struct Foo2;

/// 这个结构体也不是 [bar][b]
///
/// [b]: Bar
pub struct Foo3;

/// 这个结构体也不是 [`Bar`]
pub struct Foo4;

/// 这个结构体*就是* [`Bar`]！
pub struct Bar;
```

与普通 Markdown 不同，`[bar][Bar]` 语法也受支持，无需 `[Bar]: ...` 引用链接。

链接周围的反引号会被去掉，因此 ``[`Option`]`` 会正确链接到 `Option`。

## 有效链接 {#valid-links}

你可以引用作用域中的任何内容，并使用路径，包括 `Self`、`self`、`super` 和 `crate`。关联项（函数、类型和常量）受支持，但[不适用于 blanket trait 实现][#79682]。Rustdoc 还支持链接到[标准库文档](https://doc.rust-lang.org/std/index.html#primitives)中列出的所有原语类型。

[#79682]: https://github.com/rust-lang/rust/pull/79682

你也可以引用带泛型参数的项，如 `Vec<T>`。链接会像写成 ``[`Vec<T>`](Vec)`` 一样解析。完全限定语法（例如 `<Vec as IntoIterator>::into_iter()`）[尚不支持][fqs-issue]。

[fqs-issue]: https://github.com/rust-lang/rust/issues/74563

```rust,edition2018
use std::sync::mpsc::Receiver;

/// 这是带 [`std::future`] 支持的 [`Receiver<T>`] 版本。
///
/// 你可以调用 [`Self::recv()`] 获得一个 [`std::future::Future`]。
pub struct AsyncReceiver<T> {
    sender: Receiver<T>
}

impl<T> AsyncReceiver<T> {
    pub async fn recv() -> T {
        unimplemented!()
    }
}
```

Rustdoc 允许使用 URL 片段标识符，就像普通链接一样：

```rust
/// 这是 [positional parameters] 的一种特殊实现。
///
/// [positional parameters]: std::fmt#formatting-parameters
struct MySpecialFormatter;
```

## 命名空间与消歧符 {#namespaces-and-disambiguators}

Rust 中的路径有三个命名空间：类型、值和宏。项名在同一命名空间内必须唯一，但可以与其他命名空间中的项重叠。若有歧义，rustdoc 会警告并建议消歧符。

```rust
/// 另见：[`Foo`](struct@Foo)
struct Bar;

/// 这与 [`Foo`](fn@Foo) 不同
struct Foo {}

fn Foo() {}
```

这些前缀在文档显示时会被去掉，因此 `[struct@Foo]` 会渲染为 `Foo`。可用的前缀有：`struct`、`enum`、`trait`、`union`、`mod`、`module`、`const`、`constant`、`fn`、`function`、`field`、`variant`、`method`、`derive`、`type`、`value`、`macro`、`tyalias`、`typealias`、`prim` 或 `primitive`。

也可以通过在函数名后加 `()` 为函数消歧，或在宏名后加 `!` 为宏消歧。宏的 `!` 后面可以跟 `()`、`{}` 或 `[]`。示例：

```rust
/// 这与 [`foo!()`] 不同。
fn foo() {}

/// 这与 [`foo()`] 不同
macro_rules! foo {
  () => {}
}
```

有一种情况会自动消歧：若某个文档内链接同时解析为 trait 和 derive 过程宏。此时总是生成指向 trait 的链接，且不会发出「缺少消歧」警告。一个好例子是链接到 `Clone` trait：也存在 `Clone` 过程宏，但这种情况下会忽略它。若要链接到过程宏，可以使用 `macro@` 消歧符。

## 警告、重导出与作用域 {#warnings-re-exports-and-scoping}

链接在项定义所在模块的作用域中解析，即使该项被重导出也是如此。若来自另一个 crate 的链接解析失败，不会给出警告。

```rust,edition2018
mod inner {
    /// 链接到 [f()]
    pub struct S;
    pub fn f() {}
}
pub use inner::S; // 指向 `f` 的链接仍会正确解析
```

重导出项时，rustdoc 允许为其添加额外文档。这些额外文档在重导出的作用域中解析，而不是在原始作用域中，从而允许你链接到新 crate 中的项。若新链接解析失败，仍会给出警告。

```rust
/// 另见 [foo()]
pub use std::process::Command;

pub fn foo() {}
```

这对过程宏尤其有用，因为过程宏必须始终定义在自己的专用 crate 中。

注意：由于 Rust 中 `macro_rules!` 宏的作用域方式，`macro_rules!` 宏的文档内链接会[相对于 crate 根][#72243]解析，而不是相对于其定义所在的模块。

若链接看起来「不够像」文档内链接，会被忽略且不给出警告，即使链接解析失败也是如此。例如，任何包含 `/` 或 `[]` 字符的链接都会被忽略。

[#72243]: https://github.com/rust-lang/rust/issues/72243

## 无法生成文档内链接时会发生什么 {#what-happens-in-case-an-intra-doc-link-cannot-be-generated}

在某些情况下（例如 `cfg` 之后的项），无法生成指向该项的文档内链接。Markdown 中有多种创建链接的方式，取决于你使用的方式，此时渲染结果会不同：

```md
1. [a]
2. [b][c]
3. [d](e)
4. [f]

[f]: g
```

`1.` 和 `2.` 会在渲染文档中原样显示（即 `[a]` 和 `[b][c]`），而 `3.` 和 `4.` 会被替换为链接：`[d](e)` 指向 `e`，`[f]` 指向 `g`。
