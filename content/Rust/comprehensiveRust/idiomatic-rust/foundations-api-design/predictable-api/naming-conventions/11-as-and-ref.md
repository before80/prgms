+++
title = "2.2.1.11 As 与 Ref"
date = 2026-08-11T11:30:00+08:00
weight = 411
type = "docs"
description = "11-As 与 Ref — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/as-and-ref.html](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions/as-and-ref.html)

# 2.2.1.11 As 与 Ref

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
impl<T> Rc<T> {
    // 在容器类型上非常常见，注意 Option 上也有。
    fn as_ref(&self) -> &T;

    fn as_ptr(&self) -> *const T;
}

impl<T> Option<T> {
    fn as_ref(&self) -> Option<&T>;

    fn as_slice(&self) -> &[T];
}
```

> - 返回对所含主要数据一块的借用的方法。
>
> - 借用关系通常很直接：返回值是借用 `self` 的引用。
>
> - 返回值也可以仅在逻辑上借用 `self`，例如 `as_ptr()` 方法返回不安全指针。借用检查器不跟踪指针的借用。
>
> - 实现 “as” 方法的类型应包含一块正在被借出的主要数据。
>
>   - 若数据类型是许多字段的聚合，且没有明显的主字段，“as” 命名约定不适用。
>
>   - 若有两个需要区分的引用 getter，使用 `_ref` 后缀。

