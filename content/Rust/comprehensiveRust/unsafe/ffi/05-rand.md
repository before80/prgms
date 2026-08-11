+++
title = "9.6 封装 `srand(3)` 与 `rand(3)`"
date = 2026-08-11T11:30:00+08:00
weight = 572
type = "docs"
description = "05-封装 `srand(3)` 与 `rand(3)` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/rand.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/ffi/rand.html)

# 9.6 封装 `srand(3)` 与 `rand(3)`

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
use libc::{rand, srand};

// unsafe extern "C" {
//     /// 为随机数生成器设置种子
//     fn srand(seed: std::ffi::c_uint);

//     fn rand() -> std::ffi::c_int;
// }

fn main() {
    unsafe { srand(12345) };

    let a = unsafe { rand() as i32 };
    println!("{a:?}");
}
```

> 本幻灯片旨在说明：若包装器编写不当，很容易触发未定义行为。我们将看到触发类型安全问题有多么容易。
>
> 说明 `rand` 与 `srand` 由 C 标准库（libc）提供。
>
> 说明这些函数由 libc crate 导出，但我们也可以手动编写 FFI 包装器。
>
> 演示从导出项调用这些函数。
>
> 代码能编译，因为 libc 默认链接到 Rust 程序。
>
> 说明若使用错误的类型，Rust 也会信任你。
>
> 将 `fn rand() -> std::ffi::c_int;` 修改为返回 `char`。
>
> 避免类型安全问题，是使用工具生成包装器而非手工编写的原因之一。

