+++
title = "1.7 记录"
date = 2026-08-11T11:30:00+08:00
weight = 326
type = "docs"
description = "记录 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/aps/logging.html](https://google.github.io/comprehensive-rust/bare-metal/aps/logging.html)

# 1.7 记录

如果能够使用 [ 中的日志记录宏，那就太好了`log`][1] 板条箱。
我们可以通过实施来做到这一点`Log`特征。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use crate::pl011::Uart;
use core::fmt::Write;
use log::{LevelFilter, Log, Metadata, Record, SetLoggerError};
use spin::mutex::SpinMutex;

static LOGGER: Logger = Logger { uart: SpinMutex::new(None) };

struct Logger {
    uart: SpinMutex<Option<Uart<'static>>>,
}

impl Log for Logger {
    fn enabled(&self, _metadata: &Metadata) -> bool {
        true
    }

    fn log(&self, record: &Record) {
        writeln!(
            self.uart.lock().as_mut().unwrap(),
            "[{}] {}",
            record.level(),
            record.args()
        )
        .unwrap();
    }

    fn flush(&self) {}
}

/// 初始化 UART 记录器。
pub fn init(
    uart: Uart<'static>,
    max_level: LevelFilter,
) -> Result<(), SetLoggerError> {
    LOGGER.uart.lock().replace(uart);

    log::set_logger(&LOGGER)?;
    log::set_max_level(max_level);
    Ok(())
}
```

> - 第一个解开在`log`会成功，因为我们初始化了`LOGGER`前
>   呼叫`set_logger`。第二个会成功，因为`Uart::write_str`总是
>   回报`Ok`.


[1]: https://crates.io/crates/log
