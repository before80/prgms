+++
title = "2.4 练习：日志过滤器"
date = 2026-08-11T11:30:00+08:00
weight = 100
type = "docs"
description = "练习：日志过滤器 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/closures/exercise.html](https://google.github.io/comprehensive-rust/closures/exercise.html)

# 2.4 练习：日志过滤器

基于今天上午的泛型日志器，实现一个 `Filter`：用闭包过滤日志消息，把通过过滤谓词的消息发给内部日志器。

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

// TODO: 定义并实现 `Filter`。

fn main() {
    let logger = Filter::new(StderrLogger, |_verbosity, msg| msg.contains("yikes"));
    logger.log(5, "FYI");
    logger.log(1, "yikes, something went wrong");
    logger.log(2, "uhoh");
}
```
