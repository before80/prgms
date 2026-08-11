+++
title = "3.2.5 用 forget 拆除 Drop Bomb"
date = 2026-08-11T11:30:00+08:00
weight = 435
type = "docs"
description = "05-用 forget 拆除 Drop Bomb — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/raii/drop_bomb_forget.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/raii/drop_bomb_forget.html)

# 3.2.5 用 forget 拆除 Drop Bomb

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::io::{self, Write};

struct Transaction;

impl Transaction {
    fn start() -> Self {
        Transaction
    }

    fn commit(self) -> io::Result<()> {
        writeln!(io::stdout(), "COMMIT")?;

        // 通过阻止 Drop 运行来拆除 drop bomb。
        std::mem::forget(self);

        Ok(())
    }
}

impl Drop for Transaction {
    fn drop(&mut self) {
        // 这就是「drop bomb」
        panic!("Transaction dropped without commit!");
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

> 本示例去掉了上一页的标志，让 drop 方法无条件 panic。为在成功提交时避免该 panic，commit 方法现在取得事务的所有权并调用
> [`std::mem::forget`](https://doc.rust-lang.org/std/mem/fn.forget.html)，
> 从而阻止运行 `Drop::drop()` 方法。
>
> 若被 forget 的值拥有本应在其 `drop()` 实现中释放的堆分配内存，后果之一是内存泄漏。上例中的 `Transaction` 不属于这种情况，因为它不拥有任何堆内存。
>
> 通过战术性地使用 `mem::forget()`，我们可以避免需要运行时标志。当事务成功提交时，对值调用 `std::mem::forget` 即可拆除 drop bomb，阻止其 `Drop` 实现运行。

