+++
title = "6 日志"
date = 2026-08-11T11:30:00+08:00
weight = 233
type = "docs"
description = "03-日志 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/logging.html](https://google.github.io/comprehensive-rust/android/logging.html)

# 6 日志

应使用 `log` crate，以便自动将日志输出到 `logcat`（设备上）或 `stdout`（主机上）：

_hello_rust_logs/Android.bp_：

```javascript
rust_binary {
    name: "hello_rust_logs",
    crate_name: "hello_rust_logs",
    srcs: ["src/main.rs"],
    rustlibs: [
        "liblog_rust",
        "liblogger",
    ],
    host_supported: true,
}
```

_hello_rust_logs/src/main.rs_：

```rust,ignore
// Copyright 2022 Google LLC
// SPDX-License-Identifier: Apache-2.0
//! Rust logging demo.

use log::{debug, error, info};

/// Logs a greeting.
fn main() {
    logger::init(
        logger::Config::default()
            .with_tag_on_device("rust")
            .with_max_level(log::LevelFilter::Trace),
    );
    debug!("Starting program.");
    info!("Things are going fine.");
    error!("Something went wrong!");
}
```

在设备上构建、推送并运行该二进制：

```shell
m hello_rust_logs
adb push "$ANDROID_PRODUCT_OUT/system/bin/hello_rust_logs" /data/local/tmp
adb shell /data/local/tmp/hello_rust_logs
```

日志会出现在 `adb logcat` 中：

```shell
adb logcat -s rust
```

```text
09-08 08:38:32.454  2420  2420 D rust: hello_rust_logs: Starting program.
09-08 08:38:32.454  2420  2420 I rust: hello_rust_logs: Things are going fine.
09-08 08:38:32.454  2420  2420 E rust: hello_rust_logs: Something went wrong!
```

> - `liblogger` 中的 logger 实现只需要出现在最终二进制里；若从库中打日志，只需依赖 `log` 门面 crate。

