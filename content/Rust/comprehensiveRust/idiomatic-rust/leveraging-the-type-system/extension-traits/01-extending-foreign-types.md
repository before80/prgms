+++
title = "3.3.1 扩展外来类型"
date = 2026-08-11T11:30:00+08:00
weight = 440
type = "docs"
description = "01-扩展外来类型 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/extension-traits/extending-foreign-types.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/extension-traits/extending-foreign-types.html)

# 3.3.1 扩展外来类型

**扩展 trait**（extension trait）是本地定义的 trait，其主要目的是给外来类型附加新方法。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
mod ext {
    pub trait StrExt {
        fn is_palindrome(&self) -> bool;
    }

    impl StrExt for str {
        fn is_palindrome(&self) -> bool {
            self.chars().eq(self.chars().rev())
        }
    }
}

fn main() {
    // 将扩展 trait 引入作用域...
    pub use ext::StrExt as _;
    // ...然后像调用固有方法一样调用其方法
    assert!("dad".is_palindrome());
    assert!(!"grandma".is_palindrome());
}
```

> - 按惯例，扩展 trait 名称会带 `Ext` 后缀。
>
>   这表明该 trait 主要用于扩展，因此不打算在定义它的 crate 之外实现。
>
>   命名约定以 [「Extension Trait」RFC][1] 为准。
>
> - 对外来类型的扩展 trait 实现必须与 trait 本身在同一 crate 中，否则会被 Rust 的
>   [_孤儿规则_][2]
>   拦住。
>
> - 调用扩展方法时，扩展 trait 必须在作用域内。
>
>   注释掉示例中的 `use` 语句，展示在未将对应扩展 trait 引入作用域时调用扩展方法会得到的编译错误。
>
> - 上例使用 [_下划线导入_][3]（`use ext::StringExt as _`）以降低与其他已导入 trait 命名冲突的可能性。
>
>   使用下划线导入时，该 trait 被视为在作用域内，你可以在实现该 trait 的类型上调用其方法。但其**符号**本身不可直接访问。这会阻止你例如在 `where` 子句中使用该 trait。
>
>   由于扩展 trait 不打算用在 `where` 子句中，惯例是通过下划线导入。


[1]: https://rust-lang.github.io/rfcs/0445-extension-trait-conventions.html
[2]: https://github.com/rust-lang/rfcs/blob/master/text/2451-re-rebalancing-coherence.md#what-is-coherence-and-why-do-we-care
[3]: https://doc.rust-lang.org/stable/reference/items/use-declarations.html#r-items.use.as-underscore
