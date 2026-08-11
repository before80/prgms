+++
title = "3.4 练习：泛型日志器"
date = 2026-08-11T11:30:00+08:00
weight = 83
type = "docs"
description = "练习：泛型日志器 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/methods-and-traits/exercise.html](https://google.github.io/comprehensive-rust/methods-and-traits/exercise.html)

# 3.4 练习：泛型日志器

让我们设计一个简单的日志工具：用带 `log` 方法的 `Logger` trait。可能需要记录进度的代码可以接收 `&impl Logger`。测试时可能把消息写到测试日志文件，生产构建则可能发送到日志服务器。

不过，下面给出的 `StderrLogger` 会记录所有消息，不论详细级别。你的任务是编写一个 `VerbosityFilter` 类型，忽略超过最大详细级别的消息。

这是一种常见模式：结构体包装某个 trait 的实现，并实现同一 trait，同时增加行为。在「泛型」小节中，我们会看到如何让包装器对所包装的类型泛型化。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
trait Logger {
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
struct VerbosityFilter {
    max_verbosity: u8,
    inner: StderrLogger,
}

// TODO: 为 `VerbosityFilter` 实现 `Logger` trait。

fn main() {
    let logger = VerbosityFilter { max_verbosity: 3, inner: StderrLogger };
    logger.log(5, "FYI");
    logger.log(2, "Uhoh");
}
```
