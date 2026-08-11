+++
title = "2.2.2.7 Copy"
date = 2026-08-11T11:30:00+08:00
weight = 421
type = "docs"
description = "07-Copy — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/copy.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/common-traits/copy.html)

# 2.2.2.7 Copy

类似 `Clone`，但表示类型可按位复制。

可派生：✅

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug, Clone, Copy)]
pub struct Copyable(u8, u16, u32, u64);

fn main() {
    let copyable = Copyable(1, 2, 3, 4);
    let copy = copyable; // 隐式复制操作
    dbg!(copyable);
    dbg!(copy);
}
```

> - `Clone` 表示显式的、用户定义的复制操作。`Copy` 表示隐式的按位复制。
>
> - 一般只应在应表现得像原始值的“纯数据”类型上实现。例如线性代数库中的原始数值类型。
>
> - 与 `Clone` 有相同注意事项：若复制值会破坏不变量，该类型不应实现 `Copy`。
>
> - 始终一起派生 `Clone` 与 `Copy`！实现 `Copy` 时*不要*手动实现 `Clone`。
>
>   - 复制操作不会调用 `clone` 方法，因此自定义 `Clone` 实现可能与隐式复制行为不同。一起派生 `Clone` 与 `Copy` 可确保调用 `clone` 与触发复制得到相同结果。
>
> - 不能在带有 `Drop` 或非 `Copy` 字段的类型上实现。
>
>   - 问问学员：为何带有堆数据的类型（`Vec`、`BTreeMap`、`Rc` 等）不能是 `Copy`？
>
>     对这些类型按位复制，意味着带有堆数据的类型不再对指针拥有独占所有权，破坏 Rust 及其生态通常维护的不变量。
>
>     多个 `Vec` 会指向同一块内存中的数据。增删数据只会更新各自 `Vec` 的长度与容量。`BTreeMap` 同理。
>
>     对 `Rc` 按位复制不会更新指针内的引用计数值，意味着可能有两个 `Rc` 实例都认为自己是该指针唯一的 `Rc`。其中一个被销毁后，其中一个的引用计数会变为 0，内部值被 drop，尽管仍有另一个 `Rc` 存活。

