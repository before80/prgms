+++
title = "4.3 泛型数据类型"
date = 2026-08-11T11:30:00+08:00
weight = 88
type = "docs"
description = "03-泛型数据类型 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/generics/generic-data.html](https://google.github.io/comprehensive-rust/generics/generic-data.html)

# 4.3 泛型数据类型

可以用泛型对具体字段类型做抽象。回到上一节的练习：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub trait Logger {
    /// 在给定详细级别记录一条消息。
    fn log(&self, verbosity: u8, message: &str);
}

struct StderrLogger;

impl Logger for StderrLogger {
    fn log(&self, verbosity: u8, message: &str) {
        eprintln!("verbosity={verbosity}: {message}");
    }
}

/// 只记录不超过给定详细级别的消息。
struct VerbosityFilter<L> {
    max_verbosity: u8,
    inner: L,
}

impl<L: Logger> Logger for VerbosityFilter<L> {
    fn log(&self, verbosity: u8, message: &str) {
        if verbosity <= self.max_verbosity {
            self.inner.log(verbosity, message);
        }
    }
}

fn main() {
    let logger = VerbosityFilter { max_verbosity: 3, inner: StderrLogger };
    logger.log(5, "FYI");
    logger.log(2, "Uhoh");
}
```

> - _问：_ 为什么 `impl<L: Logger> .. VerbosityFilter<L>` 里 `L` 写了两次？这不是冗余吗？
>   - 因为这是泛型类型的泛型实现段。它们各自独立地泛型。
>   - 意思是：这些方法对任意 `L` 都有定义。
>   - 也可以写 `impl VerbosityFilter<StderrLogger> { .. }`。
>     - `VerbosityFilter` 仍然是泛型的，你仍可用 `VerbosityFilter<f64>`，但该块中的方法只对 `VerbosityFilter<StderrLogger>` 可用。
> - 注意我们没有在 `VerbosityFilter` 类型本身上放 trait 约束。也可以把约束放在那里，但在 Rust 中一般只把 trait 约束放在 impl 块上。

