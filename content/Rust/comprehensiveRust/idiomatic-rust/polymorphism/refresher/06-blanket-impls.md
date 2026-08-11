+++
title = "4.1.6 覆盖式实现（Blanket Impl）"
date = 2026-08-11T11:30:00+08:00
weight = 475
type = "docs"
description = "06-覆盖式实现（Blanket Impl）— Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/blanket-impls.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/blanket-impls.html)

# 4.1.6 覆盖式实现（Blanket Impl）

当 trait 是本地的时，我们可以为任意多的类型实现它。能做到什么程度？

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub trait PrettyPrint {
    fn pretty_print(&self);
}

// 覆盖式实现！凡实现 Display 的类型，都实现 PrettyPrint。
impl<T> PrettyPrint for T
where
    T: std::fmt::Display,
{
    fn pretty_print(&self) {
        println!("{self}")
    }
}
```

> - 在 trait 定义处，实现的主体可以是任何东西，包括无约束的 `T`。
>
>   对一无所知的 `T` 我们什么都做不了，所以这种写法并不常见。
>
> - 带条件的覆盖式实现更有用，也更常见于阅读与编写。
>
>   这类实现会对 trait 加约束，例如 `impl <T: Display> ToString for T {...}`。
>
>   上例中，我们对所有实现 Display 的类型做了覆盖式实现；实现里从约束能得到的信息只有一点：它实现了 `Display::fmt`。
>
>   这足以写出漂亮打印到控制台的实现。
>
> - 使用这类实现时要小心，它可能阻止下游用户写出更有意义的实现。
>
>   上例没有为 `Debug` 写，因为那几乎会让所有类型都实现 `PrettyPrint`，而 `Debug` 与 `Display` 语义并不相近：前者面向调试输出，后者更偏人类可读。
>
> 参考：
>
> - https://doc.rust-lang.org/reference/glossary.html#blanket-implementation

