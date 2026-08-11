+++
title = "3.2.4 Drop Bomb"
date = 2026-08-11T11:30:00+08:00
weight = 434
type = "docs"
description = "04-Drop Bomb — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/raii/drop_bomb.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/raii/drop_bomb.html)

# 3.2.4 Drop Bomb

用 `Drop` 强制不变量并检测不正确的 API 使用。「Drop bomb」在值未经显式终结就被 drop 时会 panic。

当终结操作（如 `commit()` 或 `rollback()`）需要返回 `Result`，而 `Drop` 无法返回 `Result` 时，常使用此模式。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::io::{self, Write};

struct Transaction {
    active: bool,
}

impl Transaction {
    fn start() -> Self {
        Self { active: true }
    }

    fn commit(mut self) -> io::Result<()> {
        writeln!(io::stdout(), "COMMIT")?;
        self.active = false;
        Ok(())
    }
}

impl Drop for Transaction {
    fn drop(&mut self) {
        if self.active {
            panic!("Transaction dropped without commit!");
        }
    }
}

fn main() -> io::Result<()> {
    let tx = Transaction::start();
    // 用 `tx` 构建事务，然后提交。
    // 注释掉对 `commit` 的调用以观察 panic。
    tx.commit()?;
    Ok(())
}
```

> - 在某些系统中，值在被 drop 之前必须由特定 API 终结。
>
>   例如，`Transaction` 可能需要被提交或回滚。
>
> - Drop bomb 确保像 `Transaction` 这样的值不能在未完成状态下被静默 drop。若事务未经显式终结（例如通过 `commit()`），析构函数会 panic。
>
> - 终结操作（如 `commit()`）通常按值接受 `self`。这确保事务一旦终结，原对象就不能再被使用。
>
> - 使用此模式的常见原因是清理无法在 `Drop` 中完成，要么因为可能失败，要么因为是异步的。
>
> - 即使在公共 API 中，此模式也合适。它能帮助用户在忘记显式终结事务性对象时尽早发现 bug。
>
> - 若清理可以安全地在 `Drop` 中发生，有些 API 选择仅在 debug 构建中 panic。这是否合适取决于你的 API 必须强制的保证。
>
> - 当静默误用会导致严重的正确性或安全问题时，在 release 构建中 panic 是合理的。
>
> - 问题：为什么需要 `Transaction` 内的 `active` 标志？为什么不能让 `drop()` 无条件 panic？
>
>   期望答案：`commit()` 按值取得 `self` 并会运行 `drop()`，那样就会 panic。
>
> ## 深入探索
>
> 若干相关模式有助于强制正确拆除或防止意外 drop。
>
> - [`drop_bomb` crate](https://docs.rs/drop_bomb/latest/drop_bomb/)：一个小型工具，除非用 `.defuse()` 显式拆除，否则 drop 时会 panic。带有仅在 debug 构建中激活的 `DebugDropBomb` 变体。

