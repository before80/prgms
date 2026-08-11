+++
title = "3.6.4 Branded 之二：`PhantomData` 与生命周期子类型"
date = 2026-08-11T11:30:00+08:00
weight = 465
type = "docs"
description = "04-Branded 之二：`PhantomData` 与生命周期子类型 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/token-types/branded-02-phantomdata.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/token-types/branded-02-phantomdata.html)

# 3.6.4 Branded 之二：`PhantomData` 与生命周期子类型

思路：

- 用生命周期作为每个令牌的唯一品牌。
- 让生命周期足够不同，使它们不会隐式相互转换。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::marker::PhantomData;

#[derive(Default)]
struct InvariantLifetime<'id>(PhantomData<&'id ()>); // 主要关注点

struct Wrapper<'a> { value: u8, invariant: InvariantLifetime<'a> }

fn lifetime_separator<T>(value: u8, f: impl for<'a> FnOnce(Wrapper<'a>) -> T) -> T {
    f(Wrapper { value, invariant: InvariantLifetime::default() })
}

fn try_coerce_lifetimes<'a>(left: Wrapper<'a>, right: Wrapper<'a>) {}

fn main() {
    lifetime_separator(1, |wrapped_1| {
        lifetime_separator(2, |wrapped_2| {
            // 我们希望这不要编译
            try_coerce_lifetimes(wrapped_1, wrapped_2);
        });
    });
}
```
> - 在 Rust 中，生命周期之间可以有子类型关系。
>
>   这类关系让编译器能判断一个生命周期是否长于另一个。
>
>   判断一个生命周期是否长于另一个，也让我们能说**最短的公共生命周期是先结束的那一个**。
>
>   这在许多情况下很有用，因为这意味着两个不同的生命周期可以在它们重叠的区域内被当作相同对待。
>
>   这通常是我们想要的。但这里我们想用生命周期来区分值，从而说某个令牌只适用于单个变量，而不必为声明的每个变量创建 newtype。
>
> - **目标**：我们想要两个 Rust 编译器无法判断谁长于谁的生命周期。
>
>   我们用 `try_coerce_lifetimes` 作为编译期检查，看生命周期是否有共同的更短生命周期（即被做子类型）。
>
> - 注意：本页当前能编译；到本页结束时，应仅在注释掉 `try_coerce_lifetimes` 时才能编译。
>
> - 这段代码有两个重要部分：
>   - 传给 `lifetime_separator` 的闭包上的 `impl for<'a>` 约束。
>   - `PhantomData` 参数中生命周期的使用方式。
>
> ## 闭包上的 `for<'a>` 约束
>
> - 我们用 `for<'a>` 为函数类型引入生命周期泛型参数，并要求函数体对所有可能的生命周期都成立。
>
>   这样做也会削弱编译器对该特定生命周期在函数参数上做假设的能力，因为它必须满足 Rust 的借用检查规则，无论其参数的「真实」生命周期是什么。调用者代入实际生命周期，函数本身不能。
>
>   这类似于数学中的全称量词（Ɐ），或我们引入 `<T>` 作为类型变量的方式，但仅用于 trait 约束中的生命周期。
>
>   当我们写对类型 `T` 泛型的函数时，我们无法从函数内部确定该类型。即使我们用两个同类型参数调用 `fn foo<T, U>(first: T, second: U)`，函数体也无法判断 `T` 与 `U` 是否为同一类型。
>
>   这也防止**API 消费者**自行定义生命周期，否则他们可能绕过我们想施加的限制。
>
> ## PhantomData 与生命周期变型
>
> - 我们已经知道 `PhantomData`，它可以为原本未使用的类型或生命周期参数引入形式上的空操作使用。
>
> - 提问：我们能用 `PhantomData` 做什么？
>
>   期望提到 Typestate 模式、将拥有的值的生命周期绑定在一起。
>
> - 提问：在其他语言中，什么是子类型？
>
>   期望提到继承，即因为 `B` 是 `A` 的「子类型」，当需要类型 `A` 的值时可以使用类型 `B` 的值。
>
> - Rust 确实有子类型！但仅针对生命周期。
>
>   提问：若一个生命周期是另一生命周期的子类型，那可能意味着什么？
>
>   当一个生命周期**长于**另一生命周期时，它是另一生命周期的「子类型」。
>
> - `PhantomData` 使用的生命周期的行为，不仅取决于生命周期「来自」何处，还取决于引用如何定义。
>
>   本页能编译的原因是，`InvariantLifetime` 内生命周期的
>   [**变型（Variance）**](https://doc.rust-lang.org/stable/reference/subtyping.html#r-subtyping.variance)
>   过于宽松。
>
>   注意：不要期望学员在这里完全理解变型，先把它当作生命周期建立子类型关系能力的限制阶梯。
>
>   - 提问：我们如何让它更严格？在 Rust 中如何让引用类型更严格？
>
>   期望或演示：改为 `&'id mut ()`。这还不够！
>
>   我们需要在生命周期上使用一种
>   [**变型**](https://doc.rust-lang.org/stable/reference/subtyping.html#r-subtyping.variance)，
>   使得除了_相同生命周期_之外无法推断子类型。也就是说，编译器能知道的 `'a` 的唯一子类型就是 `'a` 本身。
>
>   注意：同样，不要试图让全班理解变型。暂时把它当作限制阶梯。
>
>   演示：从 `&'id ()`（在生命周期和类型上协变）、
>   `&'id mut ()`（在生命周期上协变，在类型上不变）、`*mut &'id mut ()`
>   （在生命周期和类型上不变），最后到 `*mut &'id ()`（在生命周期上不变，但在类型上不是）。
>
>   最后两种不应编译，这意味着我们终于找到了如何将生命周期绑定到 `PhantomData`、使它们在此上下文中无法相互比较的候选方案。
>
>   原因：`*mut` 表示
>   [可变原始指针](https://doc.rust-lang.org/reference/types/pointer.html#r-type.pointer.raw)。
>   Rust 有可变指针！但你无法在安全 Rust 中对它们推理。让这成为指向带生命周期引用的可变原始指针，会使编译器做子类型的能力复杂化，因为它无法在借用检查器内对可变原始指针推理。
>
> - 总结：我们引入了通过为 `PhantomData` 中的生命周期选择足够严格的变型，来阻止编译器判定生命周期「足够相似」的方法，从而使本页无法编译。
>
>   也就是说，我们现在可以创建能存在于同一作用域、但类型按变量自动彼此不同的变量，而无需太多样板代码。
>
> ## 深入探索
>
> - `for<'a>` 量词不仅用于函数类型。它是
>   [**高阶 trait 约束**](https://doc.rust-lang.org/reference/subtyping.html?search=Hiher#r-subtype.higher-ranked)。

