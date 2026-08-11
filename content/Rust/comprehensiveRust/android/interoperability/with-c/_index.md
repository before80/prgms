+++
title = "7.1 与 C 互操作"
date = 2026-08-11T11:30:00+08:00
weight = 235
type = "docs"
description = "与 C 互操作 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/android/interoperability/with-c.html](https://google.github.io/comprehensive-rust/android/interoperability/with-c.html)

# 7.1 与 C 互操作

Rust 完全支持链接使用 C 调用约定的目标文件。同样，你也可以导出 Rust 函数并从 C 调用它们。

若愿意，可以手工完成：

```rust
// Copyright 2022 Google LLC
// SPDX-License-Identifier: Apache-2.0
unsafe extern "C" {
    safe fn abs(x: i32) -> i32;
}

fn main() {
    let x = -42;
    let abs_x = abs(x);
    println!("{x}, {abs_x}");
}
```

我们在
[Safe FFI Wrapper 练习](../../unsafe/ffi/)
中已经见过这种写法。

> 这假设你对目标平台有完整了解。不建议用于生产。

接下来我们看更好的选项。

> - `extern` 块中的 [`"C"` 部分][extern-abi]告诉 Rust：`abs` 可以使用 C [ABI]（application binary interface，应用程序二进制接口）调用。
>
> - `safe fn abs` 部分告诉 Rust：`abs` 是安全函数。默认情况下，extern 函数是 unsafe 的，但因为对任意 `x` 调用 `abs(x)` 都不会触发未定义行为，我们可以把它声明为 safe。


[extern-abi]: https://doc.rust-lang.org/reference/items/external-blocks.html#abi
[ABI]: https://en.wikipedia.org/wiki/Application_binary_interface
