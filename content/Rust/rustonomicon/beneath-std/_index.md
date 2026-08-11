+++
title = "第12章 深入 std 之下"
date = 2026-08-06T17:08:00+08:00
weight = 62
type = "docs"
description = "不依赖 std 的可执行程序与底层"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 深入 std 之下


> 原文链接: [https://doc.rust-lang.org/nomicon/beneath-std.html](https://doc.rust-lang.org/nomicon/beneath-std.html)


　　本节记录通常由 `std` crate 提供、而 `#![no_std]` 开发者必须自行处理（即提供）以构建 `#![no_std]` 二进制 crate 的功能。

## 使用 `libc`

　　要构建 `#[no_std]` 可执行文件，需要把 `libc` 作为依赖。可在 `Cargo.toml` 中指定：

```toml
[dependencies]
libc = { version = "0.2.146", default-features = false }
```

　　注意默认特性已禁用。这是关键一步——**`libc` 的默认特性包含 `std` crate，必须禁用。**

　　或者，可使用不稳定的 `rustc_private` 私有特性，配合 `extern crate libc;`，如下例。注意 windows-msvc 目标不需要 libc，其 sysroot 中也没有 `libc` crate。下面不需要 `extern crate libc;`，在 windows-msvc 目标上写它会编译错误。

## 编写不依赖 `std` 的可执行文件

　　构建 `#![no_std]` 可执行文件可能需要 nightly 编译器，因为在许多平台上必须提供 `eh_personality` [lang item]，它是不稳定的。

　　需要为入口点定义适合目标的符号。例如 `main`、`_start`、`WinMain`，或目标相关的其他起点。此外要用 `#![no_main]` 属性，防止编译器自行生成入口点。

　　还必须定义 [panic 处理函数](panic-handler.html)。

```rust
#![feature(lang_items, core_intrinsics, rustc_private)]
#![allow(internal_features)]
#![no_std]
#![no_main]

// 在 cfg(unix) 平台上、`panic = "unwind"` 构建所必需。
#![feature(panic_unwind)]
extern crate unwind;

// 引入系统 libc，crt0.o 可能需要。
#[cfg(not(windows))]
extern crate libc;

use core::ffi::{c_char, c_int};
use core::panic::PanicInfo;

// 本程序的入口点。
#[unsafe(no_mangle)] // 确保此符号以 `main` 出现在输出中
extern "C" fn main(_argc: c_int, _argv: *const *const c_char) -> c_int {
    0
}

// 编译器会用到这些函数，但对像这样的空程序不需要。
// 通常由 `std` 提供。
#[lang = "eh_personality"]
fn rust_eh_personality() {}
#[panic_handler]
fn panic_handler(_info: &PanicInfo) -> ! { core::intrinsics::abort() }
```

　　若目标没有通过 rustup 提供标准库二进制发布（可能意味着你在自行构建 `core` crate），且需要 compiler-rt 内建函数（即构建可执行文件时出现链接错误：``undefined reference to `__aeabi_memcpy'``），需要手动链接 [`compiler_builtins` crate] 以获取这些内建函数并解决链接错误。

[`compiler_builtins` crate]: https://crates.io/crates/compiler_builtins
[lang item]: https://doc.rust-lang.org/nightly/unstable-book/language-features/lang-items.html
