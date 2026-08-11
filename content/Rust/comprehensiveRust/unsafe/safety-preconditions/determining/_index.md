+++
title = "4.3 确定前置条件"
date = 2026-08-11T11:30:00+08:00
weight = 521
type = "docs"
description = "确定前置条件 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/safety-preconditions/determining.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/safety-preconditions/determining.html)

# 4.3 确定前置条件

在哪里查找安全前置条件？

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let b: *mut i32 = std::ptr::null_mut();
    println!("{:?}", b.as_mut());
}
```

> 尝试编译程序以触发编译器错误（"error\[E0133\]: call to unsafe function ..."）。
>
> 提问：「如果想了解某个函数的前置条件，你会去哪里查？这里我们需要理解何时可以安全地将 null 指针转换为可变引用。」
>
> 查找位置：
>
> - 函数的 API 文档，尤其是其安全（Safety）章节
> - 源代码及其内部的 SAFETY 注释
> - 模块文档
> - Rust Reference（Rust 参考手册）
>
> 查阅 `as_mut` 方法的[文档][the documentation]。
>
> 高亮 Safety 章节。
>
> > **Safety**
> >
> > 调用此方法时，你必须确保指针要么为 null，要么可以转换为引用。
>
> 点击「convertible to a reference」（可转换为引用）超链接，跳转到「Pointer to reference conversion」（指针到引用转换）。
>
> 追踪将指针转换为引用的规则，即是否「可解引用」（dereferenceable）。
>
> 思考这段摘录（Rust 1.90.0）的含义：「你必须强制执行 Rust 的别名规则。确切的别名规则尚未最终确定，……」


[the documentation]: https://doc.rust-lang.org/std/primitive.pointer.html#method.as_mut
