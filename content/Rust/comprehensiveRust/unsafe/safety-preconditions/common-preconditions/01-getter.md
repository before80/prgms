+++
title = "4.1.1 Getter 示例"
date = 2026-08-11T11:30:00+08:00
weight = 518
type = "docs"
description = "01-Getter 示例 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/safety-preconditions/getter.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/safety-preconditions/getter.html)

# 4.1.1 Getter 示例

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 返回 `arr` 中 `index` 位置的元素
unsafe fn get(arr: *const i32, index: usize) -> i32 {
    unsafe { *arr.add(index) }
}
```

> 「安全前置条件是指代码上必须满足的条件，以维持 Rust 的安全保证。
>
> 「你很可能会发现，安全前置条件与 Safe Rust 的规则之间有很强的对应关系。」
>
> 提问：「`get` 的安全前置条件有哪些？」
>
> - 指针 `arr` 非 null、正确对齐，且指向 `i32` 数组
> - `index` 在边界内
>
> 添加 SAFETY 注释：
>
> ```rust
> // Copyright 2026 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> /// 返回 `arr` 中 `index` 位置的元素
> ///
> /// # 安全
> ///
> /// - `arr` 非 null、正确对齐，且指向有效的 `i32`
> /// - `index` 在数组边界内
> unsafe fn get(arr: *const i32, index: usize) -> i32 {
>     // SAFETY：调用方保证 index 在边界内
>     unsafe { *arr.add(index) }
> }
> ```
>
> 可选：在 debug 构建中添加运行时检查，以提供额外的健壮性。
>
> ```rust
> // Copyright 2026 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> debug_assert!(!arr.is_null());
> debug_assert_eq!(arr as usize % std::mem::align_of::<i32>(), 0);
> ```

