+++
title = "3.4 封装"
date = 2026-08-11T11:30:00+08:00
weight = 174
type = "docs"
description = "04-封装 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/modules/encapsulation.html](https://google.github.io/comprehensive-rust/modules/encapsulation.html)

# 3.4 封装

与模块中的项一样，结构体字段默认也是私有的。私有字段在模块其余部分（包括子模块）中同样可见。这让我们能够封装结构体的实现细节，控制对外可见的数据与功能。

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
use outer::Foo;

mod outer {
    pub struct Foo {
        pub val: i32,
        is_big: bool,
    }

    impl Foo {
        pub fn new(val: i32) -> Self {
            Self { val, is_big: val > 100 }
        }
    }

    pub mod inner {
        use super::Foo;

        pub fn print_foo(foo: &Foo) {
            println!("Is {} big? {}", foo.val, foo.is_big);
        }
    }
}

fn main() {
    let foo = Foo::new(42);
    println!("foo.val = {}", foo.val);
    // let foo = Foo { val: 42, is_big: true };

    outer::inner::print_foo(&foo);
    // println!("Is {} big? {}", foo.val, foo.is_big);
}
```

> - 本页演示结构体的隐私是基于模块的。来自面向对象语言的学员可能习惯把类型本身当作封装边界；这里展示 Rust 的不同之处，以及我们仍如何实现封装（encapsulation）。
>
> - 注意 `is_big` 字段完全由 `Foo` 控制，使 `Foo` 能够控制其初始化方式，并强制所需不变量（例如仅当 `val > 100` 时 `is_big` 才为 `true`）。
>
> - 指出可以在同一模块（包括子模块）中定义辅助函数，以便访问该类型的私有字段/方法。
>
> - 第一行被注释掉的代码演示：不能用私有字段来初始化结构体。第二行演示：也不能直接访问私有字段。
>
> - 枚举不支持隐私：变体以及变体中的数据始终是公开的。
>
> ## 更多探索
>
> - 若学员想了解枚举中的隐私（或其缺失），可以提到 `#[doc_hidden]` 与 `#[non_exhaustive]`，并展示如何用它们限制对枚举的操作。
>
> - 即使 `impl` 块写在其他模块中，模块隐私规则仍然适用
>   [（playground 示例）][1]。


[1]: https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=3e61f43c88de12bcdf69c1d6df9ab3da
