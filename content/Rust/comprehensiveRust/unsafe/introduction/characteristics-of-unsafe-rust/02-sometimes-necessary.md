+++
title = "3.5.2 有时必不可少"
date = 2026-08-11T11:30:00+08:00
weight = 511
type = "docs"
description = "02-有时必不可少 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/characteristics-of-unsafe-rust/sometimes-necessary.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/introduction/characteristics-of-unsafe-rust/sometimes-necessary.html)

# 3.5.2 有时必不可少

Rust 编译器只能对它已编译的代码强制执行其规则。

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    let pid = unsafe { libc::getpid() };
    println!("{pid}");
}
```

> 「有些活动 _必须_ 使用 unsafe。」
>
> 「Rust 编译器无法验证外部函数是否符合 Rust 的内存保证。因此，调用外部函数需要 unsafe 块。」
>
> 可选内容：
>
> 「与外部环境交互通常涉及共享内存。计算机提供的接口是内存地址（指针）。」
>
> 「下面是一个示例，请求 Linux 内核写入我们控制的内存：
>
> ```rust
> // Copyright 2026 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> fn main() {
>     let mut buf = [0u8; 8];
>     let ptr = buf.as_mut_ptr() as *mut libc::c_void;
>
>     let status = unsafe { libc::getrandom(ptr, buf.len(), 0) };
>     if status > 0 {
>         println!("{buf:?}");
>     }
> }
> ```
>
> 「这次 FFI 调用进入操作系统以填充我们的缓冲区（`buf`）。除了调用外部函数，我们还必须将边界标记为 `unsafe`，因为编译器无法验证操作系统如何操作那块内存。」

