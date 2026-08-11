+++
title = "4.4 泛型 Trait"
date = 2026-08-11T11:30:00+08:00
weight = 89
type = "docs"
description = "04-泛型 Trait — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/generics/generic-traits.html](https://google.github.io/comprehensive-rust/generics/generic-traits.html)

# 4.4 泛型 Trait

Trait 也可以是泛型的，就像类型与函数一样。Trait 的参数在使用时会变成具体类型。例如 [`From<T>`][from] trait 用于定义类型转换：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub trait From<T>: Sized {
    fn from(value: T) -> Self;
}
```

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug)]
struct Foo(String);

impl From<u32> for Foo {
    fn from(from: u32) -> Foo {
        Foo(format!("Converted from integer: {from}"))
    }
}

impl From<bool> for Foo {
    fn from(from: bool) -> Foo {
        Foo(format!("Converted from bool: {from}"))
    }
}

fn main() {
    let from_int = Foo::from(123);
    let from_bool = Foo::from(true);
    dbg!(from_int);
    dbg!(from_bool);
}
```

> - `From` trait 会在课程后面介绍，但其
>   [`std` 文档中的定义][from] 很简单，这里复制出来作参考。
>
> - Trait 的实现不必覆盖所有可能的类型参数。这里 `Foo::from("hello")` 无法编译，因为没有为 `Foo` 实现 `From<&str>`。
>
> - 泛型 trait 把类型当作「输入」，而关联类型是一种「输出」类型。一个 trait 可以为不同的输入类型有多个实现。
>
> - 实际上，Rust 要求对任意类型 `T` 至多有一个匹配的 trait 实现。与某些其他语言不同，Rust 没有选择「最具体」匹配的启发式。增加该支持的工作称为
>   [特化（specialization）](https://rust-lang.github.io/rfcs/1210-impl-specialization.html)。


[from]: https://doc.rust-lang.org/std/convert/trait.From.html
