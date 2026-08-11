+++
title = "3.3.3 Trait 方法冲突"
date = 2026-08-11T11:30:00+08:00
weight = 442
type = "docs"
description = "03-Trait 方法冲突 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/extension-traits/trait-method-conflicts.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/extension-traits/trait-method-conflicts.html)

# 3.3.3 Trait 方法冲突

为同一类型实现的两个不同 trait 方法发生命名冲突时会怎样？

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
mod ext {
    pub trait Ext1 {
        fn is_palindrome(&self) -> bool;
    }

    pub trait Ext2 {
        fn is_palindrome(&self) -> bool;
    }

    impl Ext1 for str {
        fn is_palindrome(&self) -> bool {
            self.chars().eq(self.chars().rev())
        }
    }

    impl Ext2 for str {
        fn is_palindrome(&self) -> bool {
            self.chars().eq(self.chars().rev())
        }
    }
}

pub use ext::{Ext1, Ext2};

// 调用的是哪个方法？
// 来自 `Ext1` 的？还是来自 `Ext2` 的？
fn main() {
    assert!("dad".is_palindrome());
}
```

> - 你正在扩展的 trait 可能在较新版本中添加与你的扩展方法同名的新 trait 方法。或者，同一类型的另一个扩展 trait 可能定义与你的扩展方法冲突的方法名。
>
>   提问：上例会发生什么？会有编译错误吗？两个方法中哪一个优先级更高？
>
> - 编译器会拒绝该代码，因为它无法确定调用哪个方法。`Ext1` 与 `Ext2` 彼此没有更高优先级。
>
>   要解决此冲突，必须指定想用哪个 trait。
>
>   演示：改为调用 `Ext1::is_palindrome("dad")` 或 `Ext2::is_palindrome("dad")`，而不是 `"dad".is_palindrome()`。
>
>   对于签名更复杂的方法，可能需要使用更显式的
>   [完全限定语法][1]。
>
> - 演示：将 `"dad".is_palindrome()` 替换为
>   `<str as Ext1>::is_palindrome("dad")` 或
>   `<str as Ext2>::is_palindrome("dad")`。


[1]: https://doc.rust-lang.org/reference/expressions/call-expr.html#disambiguating-function-calls
