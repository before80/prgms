+++
title = "4.1.5 父 Trait（Supertrait）"
date = 2026-08-11T11:30:00+08:00
weight = 474
type = "docs"
description = "05-父 Trait（Supertrait）— Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/supertraits.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/supertraits.html)

# 4.1.5 父 Trait（Supertrait）

Trait 可以由新的 trait 扩展。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub trait Animal {
    /* 所有动物共有的方法 */
}

pub trait Mammal: Animal {
    /* 仅哺乳动物才有的方法 */
}

// 来自标准库

pub trait Ord: Eq + PartialOrd {
    /* Ord 的方法 */
}
```

> - 编写 trait 时，可以指定类型还必须实现的其它 trait。这些称为 *父 trait*（supertrait）。
>
>   上例中，任何实现 `Mammal` 的类型也必须实现 `Animal`。
>
> - 这类 trait 层次让我们能围绕复杂现实分类体系（如动物群、机器硬件、操作系统细节等）的行为来设计系统。
>
> - 这与对象继承不同！但看起来相似。
>
>   - 对象继承允许覆盖，并默认带入被继承类型的行为。
>
>   - Trait 拥有父 trait，并不意味着该 trait 能像默认实现那样覆盖方法实现。
>
> 参考：
>
> - https://doc.rust-lang.org/reference/items/traits.html?highlight=supertrait#r-items.traits.supertraits

