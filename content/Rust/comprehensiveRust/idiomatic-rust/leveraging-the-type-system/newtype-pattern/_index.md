+++
title = "3.1 Newtype 模式"
date = 2026-08-11T11:30:00+08:00
weight = 426
type = "docs"
description = "Newtype 模式 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/newtype-pattern.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/newtype-pattern.html)

# 3.1 Newtype 模式

**Newtype** 是对已有类型（常为原始类型）的包装：

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// 唯一用户标识符，实现为围绕 `u64` 的 newtype。
pub struct UserId(u64);
```

与类型别名不同，newtype 不能与被包装类型互换使用：

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub struct UserId(u64);

fn needs_user(user: UserId) {
    // ...
}

fn main() {
    needs_user(1); // 🛠️❌
}
```

Rust 编译器也不允许你直接使用底层类型上定义的方法或运算符：

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub struct UserId(u64);

fn main() {
    assert_ne!(UserId(1), UserId(2)); // 🛠️❌
}
```

> - 学员应已在「基础知识」课程中接触过 newtype 模式，当时学习了
>   [元组结构体](../../user-defined-types/tuple-structs.md)。
>
> - 运行示例，向学员展示编译器给出的错误信息。
>
> - 把示例改成用类型别名而非 newtype，例如 `type MessageId = u64`。修改后的示例应能通过编译，从而突出两种做法的差异。
>
> - 强调：开箱即用的 newtype 本身没有附着行为。你需要有意识地决定愿意从底层类型转发哪些方法和运算符。在 `UserId` 例子中，允许 `UserId` 之间比较是合理的，但不允许加、减等算术运算。

