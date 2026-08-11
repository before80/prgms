+++
title = "3.4.2 定义 unsafe 函数"
date = 2026-08-11T11:30:00+08:00
weight = 506
type = "docs"
description = "02-定义 unsafe 函数 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/warm-up/unsafe-fn.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/warm-up/unsafe-fn.html)

# 3.4.2 定义 unsafe 函数

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 将可空指针转换为引用。
///
/// 当 `p` 为 null 时返回 `None`，否则将 `val` 包装在 `Some` 中。
fn ptr_to_ref<'a, T>(ptr: *mut T) -> Option<&'a mut T> {
    if ptr.is_null() {
        None
    } else {
        // SAFETY: `ptr` 非 null
        unsafe { Some(&mut *ptr) }
    }
}
```

> 「这段代码看起来像是 safe 代码，但实际上它需要 unsafe 块。」
>
> 强调解引用操作，即 unsafe 块内的 `*ptr`。
>
> 「调用者必须确保 `ptr` 为 null，或可以安全地转换为引用。」
>
> 「这可能违反直觉，但许多指针无法转换为引用。」
>
> 「除其他问题外，指针可能指向任意比特而非有效值。Rust 不允许这种情况，本函数需要防范这一点。」
>
> 「因此，作为 API 设计者，我们有两条路。要么尝试承担防范无效输入的责任，要么用 `unsafe` 关键字将责任转移给调用者。」
>
> 「第一条路很难。我们接受泛型类型 T，即所有实现 `Sized` 的类型。类型太多了！」
>
> 「因此，第二条路更合理。」
>
> _补充内容（时间允许时）_
>
> 「顺便说一句，若你对指针细节以及转换为引用的规则感兴趣，标准库有大量有用文档。你也应查阅 `std::pointer` 上许多方法的源代码。」
>
> 「例如，本页幻灯片上的 `ptr_to_ref` 函数在标准库中实际存在，即指针上的 `as_mut` 方法。」
>
> 打开 [std::pointer.as_mut] 的文档，并强调 Safety 部分。


[std::pointer.as_mut]: https://doc.rust-lang.org/std/primitive.pointer.html#method.as_mut
