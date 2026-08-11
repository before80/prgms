+++
title = "2.1 最小示例"
date = 2026-08-11T11:30:00+08:00
weight = 296
type = "docs"
description = "01-最小示例 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/minimal.html](https://google.github.io/comprehensive-rust/bare-metal/minimal.html)

# 2.1 最小示例

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#![no_main]
#![no_std]

use core::panic::PanicInfo;

#[panic_handler]
fn panic(_panic: &PanicInfo) -> ! {
    loop {}
}
```

> - 这会编译成一个空二进制。
> - `std` 提供了 panic handler；没有它就必须自己提供。
> - 也可以由其他 crate 提供，例如 `panic-halt`。
> - 取决于目标平台，你可能需要以 `panic = "abort"` 编译，以避免与 `eh_personality` 相关的错误。
> - 注意这里没有 `main` 或其他入口点；需要自行定义入口。这通常涉及链接脚本和一些汇编，把环境准备好再交给 Rust 代码运行。

