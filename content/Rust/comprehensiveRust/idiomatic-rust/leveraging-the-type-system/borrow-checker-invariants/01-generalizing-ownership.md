+++
title = "3.5.1 生命周期与借用：抽象规则"
date = 2026-08-11T11:30:00+08:00
weight = 454
type = "docs"
description = "01-生命周期与借用：抽象规则 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/borrow-checker-invariants/generalizing-ownership.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/borrow-checker-invariants/generalizing-ownership.html)

# 3.5.1 生命周期与借用：抽象规则

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
// 内部数据类型，用来有东西可持有。
pub struct Internal;
// 「外部」数据。
pub struct Data(Internal);

fn shared_use(value: &Data) -> &Internal {
    &value.0
}
fn exclusive_use(value: &mut Data) -> &mut Internal {
    &mut value.0
}
fn deny_future_use(value: Data) {}

fn demo_exclusive() {
    let mut value = Data(Internal);
    let shared = shared_use(&value);
    // let exclusive = exclusive_use(&mut value); // ❌🔨
    let shared_again = shared;
}

fn demo_denied() {
    let value = Data(Internal);
    deny_future_use(value);
    // let shared = shared_use(&value); // ❌🔨
}

# fn main() {}
```

> - 本例将借用检查器规则从引用重新框定为非内存安全场景下的语义含义。
>
>   没有发生任何修改，也没有跨线程发送任何东西。
>
> - 在 Rust 的借用检查器中，我们有三种「取得」值的方式：
>
>   - 拥有的值 `T`。作用域结束时值被 drop，除非它被返回到另一作用域。
>
>   - 共享引用 `&T`。允许别名，但在共享引用使用期间阻止可变访问。
>
>   - 可变引用 `&mut T`。同一时刻对一个值只允许存在一个，但可用于创建共享引用。
>
> - 提问：`demo` 函数中两行被注释掉的代码会导致编译错误，为什么？
>
>   `demo_exclusive`：因为取得 `exclusive` 引用后，`shared` 值仍然被别名。
>
>   `demo_denied`：因为在从 `&value` 取得共享引用之前一行，`value` 已被消费。
>
> - 记住每个 `&T` 和 `&mut T` 都有生命周期，只是用户多数时候不必标注或考虑它。
>
>   我们很少指定生命周期，因为 Rust 编译器在多数情况下允许我们**省略**它们。参见：
>   [生命周期省略](../../../lifetimes/lifetime-elision.md)

