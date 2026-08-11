+++
title = "3.3.4 扩展其他 Trait"
date = 2026-08-11T11:30:00+08:00
weight = 443
type = "docs"
description = "04-扩展其他 Trait — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/extension-traits/extending-other-traits.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/extension-traits/extending-other-traits.html)

# 3.3.4 扩展其他 Trait

与类型类似，有时希望**扩展外来 trait**。特别是，给给定 trait 的**所有**实现者附加新方法。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
mod ext {
    use std::fmt::Display;

    pub trait DisplayExt {
        fn quoted(&self) -> String;
    }

    impl<T: Display> DisplayExt for T {
        fn quoted(&self) -> String {
            format!("'{}'", self)
        }
    }
}

pub use ext::DisplayExt as _;

assert_eq!("dad".quoted(), "'dad'");
assert_eq!(4.quoted(), "'4'");
assert_eq!(true.quoted(), "'true'");
```

> - 强调我们如何一次为**多个**类型添加新行为。可对字符串切片、数字和布尔值调用 `.quoted()`，因为它们都实现了 `Display` trait。
>
>   这种扩展 trait 模式变体使用
>   [_blanket 实现_][1]。
>
>   Blanket 实现为满足 `impl` 块中指定 trait 约束的所有类型 `T` 实现某个 trait。本例中，唯一要求是 `T` 实现 `Display` trait。
>
> - 引导学生注意 `DisplayExt::quoted` 的实现：除了实现 `Display` 之外，我们不能对 `T` 做任何假设。所有逻辑必须要么使用 `Display` 的方法，要么使用不要求其他 trait 的函数/宏。
>
>   例如，我们可以对 `T` 调用 `format!`，但不能调用 `.to_uppercase()`，因为它不一定是 `String`。
>
>   我们可以对 `T` 引入额外的 trait 约束，但这会限制能利用该扩展 trait 的类型集合。
>
> - 按惯例，扩展 trait 以它所扩展的 trait 命名，后接 `Ext` 后缀。上例中为 `DisplayExt`。
>
> - 有整类 crate 用新功能扩展标准库 trait。
>
>   - `itertools` crate 提供扩展 `Iterator` 的 `Itertools` trait。它添加许多迭代器适配器，如 `interleave` 和 `unique`。它为用方法链构建的迭代器管道提供新的算法构件。
>
>   - `futures` crate 提供 `FutureExt` trait，用新的组合子与辅助方法扩展 `Future` trait。
>
> ## 深入探索
>
> - 库可用扩展 trait 区分稳定方法与实验性方法。
>
>   稳定方法是 trait 定义的一部分。
>
>   实验性方法通过另一库中定义的扩展 trait 提供，稳定性策略更宽松。一些实用方法在被证明有用且设计完善后，会被「提升」到核心 trait 定义中。
>
> - 扩展 trait 可用于将 [dyn 不兼容的 trait][2] 一分为二：
>
>   - **dyn 兼容的核心**，仅包含满足 dyn 兼容性要求的方法。
>   - **扩展 trait**，包含其余非 dyn 兼容的方法（例如带泛型参数的方法）。
>
> - 实现核心 trait 的具体类型将能调用所有方法，这得益于扩展 trait 的 blanket impl。Trait 对象（`dyn CoreTrait`）将能调用核心 trait 上的所有方法，以及扩展 trait 上不要求 `Self: Sized` 的那些方法。


[1]: https://doc.rust-lang.org/stable/reference/glossary.html#blanket-implementation
[`itertools`]: https://docs.rs/itertools/latest/itertools/
[`Itertools`]: https://docs.rs/itertools/latest/itertools/trait.Itertools.html
[`futures`]: https://docs.rs/futures/latest/futures/
[`FutureExt`]: https://docs.rs/futures/latest/futures/future/trait.FutureExt.html
[`Future`]: https://docs.rs/futures/latest/futures/future/trait.Future.html
[2]: https://doc.rust-lang.org/reference/items/traits.html#r-items.traits.dyn-compatible
