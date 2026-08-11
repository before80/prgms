+++
title = "4.6 `dyn Trait`"
date = 2026-08-11T11:30:00+08:00
weight = 91
type = "docs"
description = "06-`dyn Trait` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/generics/dyn-trait.html](https://google.github.io/comprehensive-rust/generics/dyn-trait.html)

# 4.6 `dyn Trait`

除了通过泛型用 trait 做静态分发外，Rust 还支持通过 trait 对象做类型擦除的动态分发：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
struct Dog {
    name: String,
    age: i8,
}
struct Cat {
    lives: i8,
}

trait Pet {
    fn talk(&self) -> String;
}

impl Pet for Dog {
    fn talk(&self) -> String {
        format!("Woof, my name is {}!", self.name)
    }
}

impl Pet for Cat {
    fn talk(&self) -> String {
        String::from("Miau!")
    }
}

// 使用泛型与静态分发。
fn generic(pet: &impl Pet) {
    println!("Hello, who are you? {}", pet.talk());
}

// 使用类型擦除与动态分发。
fn dynamic(pet: &dyn Pet) {
    println!("Hello, who are you? {}", pet.talk());
}

fn main() {
    let cat = Cat { lives: 9 };
    let dog = Dog { name: String::from("Fido"), age: 5 };

    generic(&cat);
    generic(&dog);

    dynamic(&cat);
    dynamic(&dog);
}
```

> - 泛型（包括 `impl Trait`）通过单态化为每个不同的实例化类型生成专用函数版本。这意味着在泛型函数内调用 trait 方法仍使用静态分发，因为编译器有完整类型信息，并能解析应使用该类型的哪个 trait 实现。
>
> - 使用 `dyn Trait` 时，则通过
>   [虚方法表][vtable]（vtable）做动态分发。这意味着无论传入何种 `Pet`，都只有一个版本的 `fn dynamic`。
>
> - 使用 `dyn Trait` 时，trait 对象需要某种间接层。本例中是引用，也可用 `Box` 等智能指针类型（第 3 天会演示）。
>
> - 运行时，`&dyn Pet` 表示为「胖指针」，即一对指针：一个指向实现了 `Pet` 的具体对象，另一个指向该类型对该 trait 实现的 vtable。在 `&dyn Pet` 上调用 `talk` 时，编译器在 vtable 中查找 `talk` 的函数指针，再调用该函数，并把指向 `Dog` 或 `Cat` 的指针传进去。编译器无需知道 `Pet` 的具体类型就能做到这一点。
>
> - `dyn Trait` 被认为是「类型擦除」的，因为我们不再在编译期知道具体类型是什么。
>
> [vtable]: https://en.wikipedia.org/wiki/Virtual_method_table

