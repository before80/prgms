+++
title = "4.1.1 Trait"
date = 2026-08-11T11:30:00+08:00
weight = 470
type = "docs"
description = "01-Trait — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/traits.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/traits.html)

# 4.1.1 Trait

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
trait Receiver {
    fn send(&self, message: &str);
}

struct EmailAddress(String);

impl Receiver for EmailAddress {
    fn send(&self, message: &str) {
        println!("Email to {}: {}", self.0, message);
    }
}

struct ChatId {
    uuid: [u8; 16],
}

impl Receiver for ChatId {
    fn send(&self, message: &str) {
        println!("Chat message sent to {:?}: {}", self.uuid, message);
    }
}
```

> - Rust 的多态与泛型概念很大程度上围绕 trait 展开。
>
> - Trait 是泛型上下文中对类型提出的要求。
>
> - 这些要求很像经过编译期检查的鸭子类型（duck typing）。
>
>   鸭子类型来自动态、无类型语言（如 Python）的实践：「走起来像鸭子、叫起来像鸭子，那它就是鸭子。」
>
>   也就是说，只要类型具备函数所期望的方法和字段，就都是该函数的合法输入。若某类型实现了这些方法，在鸭子类型语境下它就是那种类型。
>
>   Trait 的行为类似静态的鸭子类型：我们指定的是行为而非具体类型，但又能在编译期检查该行为是否真的存在。
>
> - 换一种说法：trait 像一组命题的集合；为类型实现 trait，就是证明该类型可以用于任何要求该 trait 的地方。
>
>   Trait 有必须实现的方法；实现这些方法，就是证明该类型具备所需行为。
>
> 参考：
>
> - https://doc.rust-lang.org/reference/items/traits.html

