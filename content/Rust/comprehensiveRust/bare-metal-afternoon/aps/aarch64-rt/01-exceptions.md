+++
title = "1.9.1 例外情况"
date = 2026-08-11T11:30:00+08:00
weight = 330
type = "docs"
description = "01-例外情况 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/aps/aarch64-rt/exceptions.html](https://google.github.io/comprehensive-rust/bare-metal/aps/aarch64-rt/exceptions.html)

# 1.9.1 例外情况

`aarch64-rt`提供一个特征来定义异常处理程序，以及一个宏
生成异常向量的汇编代码以调用它们。

该特征对每个方法都有默认实现，这只会引起恐慌，所以我们
可以省略我们不希望发生的异常的方法。

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
use aarch64_rt::{ExceptionHandlers, RegisterStateRef, exception_handlers};
use log::error;
use smccc::Hvc;
use smccc::psci::system_off;

struct Handlers;

impl ExceptionHandlers for Handlers {
    extern "C" fn sync_current(_state: RegisterStateRef) {
        error!("sync_current");
        system_off::<Hvc>().unwrap();
    }

    extern "C" fn irq_current(_state: RegisterStateRef) {
        error!("irq_current");
        system_off::<Hvc>().unwrap();
    }

    extern "C" fn fiq_current(_state: RegisterStateRef) {
        error!("fiq_current");
        system_off::<Hvc>().unwrap();
    }

    extern "C" fn serror_current(_state: RegisterStateRef) {
        error!("serror_current");
        system_off::<Hvc>().unwrap();
    }
}

exception_handlers!(Handlers);
```

> - 这`exception_handlers`宏生成一个`global_asm!`块与
>   调用 Rust 代码的异常向量，类似于`exceptions.S`我们
>   以前有过。
> - `RegisterStateRef`包装对寄存器所在堆栈帧的引用
>   当异常发生时，值由汇编代码保存。这可以是
>   例如，用于从较低层提取 SMC 或 HVC 调用的参数
>   EL，并更新异常处理程序返回时要恢复的值。

