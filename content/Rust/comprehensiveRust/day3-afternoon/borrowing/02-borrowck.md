+++
title = "2.2 借用检查"
date = 2026-08-11T11:30:00+08:00
weight = 143
type = "docs"
description = "02-借用检查 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/borrowing/borrowck.html](https://google.github.io/comprehensive-rust/borrowing/borrowck.html)

# 2.2 借用检查

Rust 的_借用检查器_（borrow checker）对借用值的方式施加约束。我们已经见过：引用不能_比_它所借用的值_活得更久_：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let x_ref = {
        let x = 10;
        &x
    };
    dbg!(x_ref);
}
```

借用检查器还强制执行第二条主要规则：_别名_（aliasing）规则。对给定值，在任意时刻：

- 你可以有一个或多个指向该值的共享引用，_或者_
- 你可以恰好有一个指向该值的独占引用。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let mut a = 10;
    let b = &a;

    {
        let c = &mut a;
        *c = 20;
    }

    dbg!(a);
    dbg!(b);
}
```

> - 「活得更久」规则在我们最初看引用时已经演示过。这里再回顾，是为了让学员看到借用检查遵循几条不同的规则来验证借用。
> - 上面的代码无法编译，因为 `a` 同时被可变借用（通过 `c`）与不可变借用（通过 `b`）。
>   - 注意：要求是冲突的引用不能在同一时刻_存在_。在哪里解引用并不重要。试着注释掉 `*c = 20`，会发现即使从未使用 `c`，编译错误仍会出现。
>   - 注意：中间引用 `c` 并非触发借用冲突所必需。把 `c` 换成对 `a` 的直接修改，也会产生类似错误。因为直接修改一个值实际上会创建一个临时的可变引用。
> - 把针对 `b` 的 `dbg!` 移到引入 `c` 的作用域之前，代码即可编译。
>   - 这样改之后，编译器意识到 `b` 只在通过 `c` 对新的可变借用 `a` 之前被使用。这是借用检查器的一项特性，称为「非词法生命周期」（non-lexical lifetimes）。
>
> ## 延伸阅读
>
> - 从技术上讲，通过再借用（re-borrowing），同一块数据上可以同时存在多个可变引用。这就是你可以把可变引用传入函数而不使原引用失效的原因。[这个 Playground 示例][1]演示了该行为。
> - Rust 用独占引用约束确保多线程代码中不会发生数据竞争，因为同一时间只有一个线程能对某块数据拥有可变访问。
> - Rust 也用该约束优化代码。例如，共享引用背后的值可以在该引用的生命周期内安全地缓存到寄存器中。
> - 结构体的字段可以彼此独立地被借用，但对结构体调用方法会借用整个结构体，可能使对单个字段的引用失效。参见[这段 Playground 代码][2]。


[1]: https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=8f5896878611566845fe3b0f4dc5af68
[2]: https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=f293a31f2d4d0d31770486247c2e8437
