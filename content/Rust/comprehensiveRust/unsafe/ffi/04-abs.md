+++
title = "9.5 封装 `abs(3)`"
date = 2026-08-11T11:30:00+08:00
weight = 571
type = "docs"
description = "04-封装 `abs(3)` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/abs.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/abs.html)

# 9.5 封装 `abs(3)`

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn abs(x: i32) -> i32;

fn main() {
    let x = -42;
    let abs_x = abs(x);
    println!("{x}, {abs_x}");
}
```

> 在本幻灯片中，我们建立编写包装器的模式。
>
> 查找函数签名的外部定义；在 `extern` 块中编写匹配的 Rust 函数；确认需要维护哪些安全不变量；判断能否将该函数标记为 safe。
>
> 注意，这_目前_还不能工作。
>
> 添加 extern 块：
>
> ```rust
> // Copyright 2026 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> unsafe extern "C" {
>     fn abs(x: i32) -> i32;
> }
> ```
>
> 说明：许多 POSIX 函数在 Rust 中可用，因为 Cargo 默认链接 C 标准库（libc），从而将其符号带入程序作用域。
>
> 在终端展示 `man 3 abs`，或打开[网页][abs]。
>
> 说明我们的函数签名必须与其定义一致：`int abs(int j);`。
>
> 将代码块更新为使用 C 类型。
>
> ```rust
> // Copyright 2026 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> use std::ffi::c_int;
>
> unsafe extern "C" {
>     fn abs(x: c_int) -> c_int;
> }
> ```
>
> 讨论理由：使用 `ffi::c_int` 可提高代码的可移植性。标准库为目标平台编译时，平台可确定其宽度。按 C 标准，`c_int` 可能被定义为 `i16`，而非常见的 `i32`。
>
> （可选）展示 [c_int 文档][c_int]，说明它是 `i32` 的类型别名。
>
> 尝试编译，触发 “error: extern blocks must be unsafe” 错误信息。
>
> 为块添加 `unsafe` 关键字：
>
> ```rust
> // Copyright 2026 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> use std::ffi::c_int;
>
> unsafe extern "C" {
>     fn abs(x: c_int) -> c_int;
> }
> ```
>
> 确认学员理解这一变更的意义：我们必须维护类型安全及其他安全前置条件。
>
> 重新编译。
>
> 为 `abs` 函数添加 `safe` 关键字：
>
> ```rust
> // Copyright 2026 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> use std::ffi::c_int;
>
> unsafe extern "C" {
>     safe fn abs(x: c_int) -> c_int;
> }
> ```
>
> 说明 `safe fn` 将 `abs` 标记为可在无 `unsafe` 块的情况下安全调用。
>
> 完整程序供参考：
>
> ```rust
> // Copyright 2026 Google LLC
> // SPDX-License-Identifier: Apache-2.0
> use std::ffi::c_int;
>
> unsafe extern "C" {
>     safe fn abs(x: c_int) -> c_int;
> }
>
> fn main() {
>     let x = -42;
>     let abs_x = abs(x);
>     println!("{x}, {abs_x}");
> }
> ```
>
> [abs]: https://www.man7.org/linux/man-pages/man3/abs.3.html
> [c_int]: https://doc.rust-lang.org/std/ffi/type.c_int.html

