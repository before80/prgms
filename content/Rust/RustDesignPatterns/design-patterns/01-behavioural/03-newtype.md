+++
title = "03-Newtype"
date = 2026-08-18T22:10:00+08:00
weight = 27
type = "docs"
description = "Newtype — Rust Design Patterns"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

> 原文链接: [https://rust-unofficial.github.io/patterns/patterns/behavioural/newtype.html](https://rust-unofficial.github.io/patterns/patterns/behavioural/newtype.html)

# Newtype

有时我们希望某个类型的行为类似于另一种类型，或在仅用类型别名不够时于编译期强制某些行为，该怎么办？

例如，出于安全考虑（如密码），我们想为 `String` 提供自定义的 `Display` 实现。

在这类情形下，可以使用 `Newtype` 模式来提供 **类型安全** 和 **封装**。

## 描述 {#description}

使用只有单个字段的元组结构体，为某类型做一个不透明包装。这会创建一种新类型，而不是类型别名（`type` 项）。

## 示例 {#example}

```rust
use std::fmt::Display;

// 创建 Newtype Password，以覆盖 String 的 Display trait
struct Password(String);

impl Display for Password {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "****************")
    }
}

fn main() {
    let unsecured_password: String = "ThisIsMyPassword".to_string();
    let secured_password: Password = Password(unsecured_password.clone());
    println!("unsecured_password: {unsecured_password}");
    println!("secured_password: {secured_password}");
}
```

```shell
unsecured_password: ThisIsMyPassword
secured_password: ****************
```

## 动机 {#motivation}

newtype 的主要动机是抽象。它允许你在类型之间共享实现细节，同时精确控制接口。通过使用 newtype 而不是把实现类型作为 API 的一部分公开，你可以在保持向后兼容的前提下更改实现。

newtype 也可用于区分单位，例如包装 `f64` 以得到可区分的 `Miles` 和 `Kilometres`。

## 优点 {#advantages}

被包装类型与包装类型并不类型兼容（与使用 `type` 相反），因此 newtype 的用户永远不会把两者「搞混」。

newtype 是零成本抽象——没有运行时开销。

隐私系统确保用户无法访问被包装类型（若字段是私有的，而默认就是私有的）。

## 缺点 {#disadvantages}

newtype 的缺点（尤其是与类型别名相比）是没有特殊的语言支持。这意味着会有*大量*样板代码。你想在被包装类型上暴露的每个方法都需要一个「透传」方法，想让包装类型也实现的每个 trait 都需要一份 impl。

## 讨论 {#discussion}

newtype 在 Rust 代码中非常常见。抽象或表示单位是最常见的用途，但也可用于其他原因：

- 限制功能（减少暴露的函数或实现的 trait），
- 让具有复制语义的类型具有移动语义，
- 通过提供更具体的类型来抽象，从而隐藏内部类型，例如：

```rust,ignore
pub struct Foo(Bar<T1, T2>);
```

这里，`Bar` 可能是某种公开的泛型类型，而 `T1` 和 `T2` 是某些内部类型。模块的用户不应知道我们用 `Bar` 来实现 `Foo`，但我们真正隐藏的是类型 `T1` 和 `T2`，以及它们如何与 `Bar` 一起使用。

## 参见 {#see-also}

- [《The Book》中的高级类型](https://doc.rust-lang.org/book/ch19-04-advanced-types.html?highlight=newtype#using-the-newtype-pattern-for-type-safety-and-abstraction)
- [Haskell 中的 Newtype](https://wiki.haskell.org/Newtype)
- [类型别名](https://doc.rust-lang.org/stable/book/ch19-04-advanced-types.html#creating-type-synonyms-with-type-aliases)
- [derive_more](https://crates.io/crates/derive_more)，一个可在 newtype 上派生许多内置 trait 的 crate。
- [Rust 中的 Newtype 模式](https://web.archive.org/web/20230519162111/https://www.worthe-it.co.za/blog/2020-10-31-newtype-pattern-in-rust.html)
