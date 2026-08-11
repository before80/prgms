+++
title = "9.4.2 不同语义"
date = 2026-08-11T11:30:00+08:00
weight = 567
type = "docs"
description = "02-不同语义 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/language-differences/semantics.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/language-differences/semantics.html)

# 9.4.2 不同语义

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
use std::ffi::{CStr, c_char};
use std::time::{SystemTime, SystemTimeError, UNIX_EPOCH};

unsafe extern "C" {
    /// 基于时间戳 `t` 创建格式化时间。
    fn ctime(t: *const libc::time_t) -> *const c_char;
}

fn now_formatted() -> Result<String, SystemTimeError> {
    let now = SystemTime::now().duration_since(UNIX_EPOCH)?;
    let seconds = now.as_secs() as i64;

    // SAFETY: `seconds` 由系统时钟生成，不会导致溢出
    let ptr = unsafe { ctime(&seconds) };

    // SAFETY: ctime 返回指向预分配（非空）缓冲区的指针
    let ptr = unsafe { CStr::from_ptr(ptr) };

    // SAFETY: ctime 使用有效的 UTF-8
    let fmt = ptr.to_str().unwrap();

    Ok(fmt.trim_end().to_string())
}

fn main() {
    let t = now_formatted();
    println!("{t:?}");
}
```

> 其他语言允许的一些构造无法用 Rust 表达。
>
> `ctime` 函数会修改调用之间共享的内部缓冲区。这无法用 Rust 的生命周期来表示。
>
> - `'static` 不适用，因为语义不同
> - `'a` 不适用，因为缓冲区在每次调用之后仍然有效

