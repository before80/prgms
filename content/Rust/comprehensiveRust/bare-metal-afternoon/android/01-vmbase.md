+++
title = "3.1 虚拟机库"
date = 2026-08-11T11:30:00+08:00
weight = 339
type = "docs"
description = "01-虚拟机库 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/android/vmbase.html](https://google.github.io/comprehensive-rust/bare-metal/android/vmbase.html)

# 3.1 虚拟机库

对于在 aarch64 上的 crosvm 下运行的 VM，[vmbase][1] 库提供了
链接器脚本和构建规则的有用默认值以及一个条目
点、UART 控制台日志记录等。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#![no_main]
#![no_std]

use vmbase::{main, println};

main!(main);

pub fn main(arg0: u64, arg1: u64, arg2: u64, arg3: u64) {
    println!("Hello world");
}
```

> - `main!` 宏标记您的主函数，将从 `vmbase` 调用
>   入口点。
> - `vmbase` 入口点处理控制台初始化，并发出
>   PSCI_SYSTEM_OFF 在主函数返回时关闭虚拟机。


[1]: https://android.googlesource.com/platform/packages/modules/Virtualization/+/refs/heads/main/libs/libvmbase/
