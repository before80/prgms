+++
title = "3.6.5 Branded 之三：实现"
date = 2026-08-11T11:30:00+08:00
weight = 466
type = "docs"
description = "05-Branded 之三：实现 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/token-types/branded-03-impl.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/token-types/branded-03-impl.html)

# 3.6.5 Branded 之三：实现

构造 branded 类型与构造非 branded 类型不同。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
# use std::marker::PhantomData;
#
# #[derive(Default)]
# struct InvariantLifetime<'id>(PhantomData<*mut &'id ()>);
struct ProvenIndex<'id>(usize, InvariantLifetime<'id>);

struct Bytes<'id>(Vec<u8>, InvariantLifetime<'id>);

impl<'id> Bytes<'id> {
    fn new<T>(
        // 我们想在此上下文中修改的数据。
        bytes: Vec<u8>,
        // 唯一地为 `Bytes` 的生命周期打品牌的函数
        f: impl for<'a> FnOnce(Bytes<'a>) -> T,
    ) -> T {
        f(Bytes(bytes, InvariantLifetime::default()),)
    }

    fn get_index(&self, ix: usize) -> Option<ProvenIndex<'id>> {
        if ix < self.0.len() { Some(ProvenIndex(ix, InvariantLifetime::default())) }
        else { None }
    }

    fn get_proven(&self, ix: &ProvenIndex<'id>) -> u8 {
        debug_assert!(ix.0 < self.0.len());
        unsafe { *self.0.get_unchecked(ix.0) }
    }
}
```

> - 动机：我们想为某类型拥有「已证明的索引」，且不希望这些索引能被同类型的不同变量使用。我们也不希望这些索引逃出作用域。
>
>   我们的 Branded 类型将是 `Bytes`：一个字节数组。
>
>   我们的 Branded 令牌将是 `ProvenIndex`：已知在范围内的索引。
>
> - 此实现有几个值得注意的部分：
>   - `new` 不返回 `Bytes`，而是要求「起始数据」和一个一次性闭包，调用时向其传入 `Bytes`。
>   - 该 `new` 函数的 trait 约束上有 `for<'a>`。
>   - 我们既有按索引取的 getter，也有按已证明索引取值的 getter。
>
> - 提问：为什么 `new` 不返回 `Bytes`？
>
>   答：因为我们需要 `Bytes` 拥有由 API 控制的唯一生命周期。
>
> - 提问：那么若 `new()` 返回 `Bytes`，会造成什么具体危害？
>
>   答：想想那个假想 `new()` 方法的签名：
>
>   `fn new<'a>() -> Bytes<'a> { ... }`
>
>   这将允许 API 用户选择生命周期 `'a` 是什么，从而剥夺我们保证不同 `Bytes` 实例之间的生命周期唯一且无法彼此做子类型的能力。
>
> - 提问：为什么我们既需要 `get_index` 又需要 `get_proven`？
>
>   期望「因为我们无法在编译期知道索引是否被占用」
>
>   提问：那么已证明索引的意义是什么？
>
>   答：在避免边界检查的同时，将哪些索引被占用的知识保持为特定于各个变量，无法被错误地用在错误的变量上。
>
>   注意：重点不仅在于避免过度使用边界检查，还在于防止索引的那种「交叉」使用。

