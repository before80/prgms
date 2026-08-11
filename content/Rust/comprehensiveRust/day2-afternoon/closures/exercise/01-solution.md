+++
title = "2.4.1 解答"
date = 2026-08-11T11:30:00+08:00
weight = 101
type = "docs"
description = "01-解答 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/closures/solution.html](https://google.github.io/comprehensive-rust/closures/solution.html)

# 2.4.1 解答

```rust
// Copyright 2025 Google LLC
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

/// 只记录匹配过滤谓词的消息。
struct Filter<L, P> {
    inner: L,
    predicate: P,
}

impl<L, P> Filter<L, P>
where
    L: Logger,
    P: Fn(u8, &str) -> bool,
{
    fn new(inner: L, predicate: P) -> Self {
        Self { inner, predicate }
    }
}
impl<L, P> Logger for Filter<L, P>
where
    L: Logger,
    P: Fn(u8, &str) -> bool,
{
    fn log(&self, verbosity: u8, message: &str) {
        if (self.predicate)(verbosity, message) {
            self.inner.log(verbosity, message);
        }
    }
}

fn main() {
    let logger = Filter::new(StderrLogger, |_verbosity, msg| msg.contains("yikes"));
    logger.log(5, "FYI");
    logger.log(1, "yikes, something went wrong");
    logger.log(2, "uhoh");
}
```

- **存储闭包：** 要在结构体中存储闭包，我们使用泛型类型参数（这里是 `P`）。这是因为 Rust 中每个闭包都有编译器生成的唯一匿名类型。
- **`Fn` trait 约束：** 约束 `P: Fn(u8, &str) -> bool` 告诉编译器：`P` 可以作为带指定参数与返回类型的函数来调用。我们用 `Fn`（而不是 `FnMut` 或 `FnOnce`），因为 `log` 取 `&self`，所以只能以不可变方式访问谓词。
- **调用字段：** 用 `(self.predicate)(...)` 调用闭包。`self.predicate` 周围的圆括号是必要的，以便区分「调用名为 `predicate` 的方法」与「调用字段本身」。

> - 讨论为何需要 `Fn`。若用 `FnMut`，`log` 就需要取 `&mut self`，这与 `Logger` trait 签名冲突。若用 `FnOnce`，就只能记录一条消息！
> - `new` 的 `impl` 块也包含约束。虽然对结构体定义本身并非严格必需（约束可以只放在使用它们的 `impl` 块上），但放在 `new` 上有助于类型推断。

