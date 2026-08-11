+++
title = "3.3 可变静态变量"
date = 2026-08-11T11:30:00+08:00
weight = 199
type = "docs"
description = "03-可变静态变量 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-rust/mutable-static.html](https://google.github.io/comprehensive-rust/unsafe-rust/mutable-static.html)

# 3.3 可变静态变量

读取不可变静态变量是安全的：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
static HELLO_WORLD: &str = "Hello, world!";

fn main() {
    println!("HELLO_WORLD: {HELLO_WORLD}");
}
```

然而，对可变静态变量的读写是 unsafe 的，因为多个线程可能在无同步的情况下并发访问，构成数据竞争（data race）。

要正确地（soundly）使用可变静态变量，需要在缺少编译器帮助的情况下自行推理并发：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
static mut COUNTER: u32 = 0;

fn add_to_counter(inc: u32) {
    // SAFETY: 没有其他线程会访问 `COUNTER`。
    unsafe {
        COUNTER += inc;
    }
}

fn main() {
    add_to_counter(42);

    // SAFETY: 没有其他线程会访问 `COUNTER`。
    unsafe {
        dbg!(COUNTER);
    }
}
```

> <summary>讲师备注</summary>
>
> - 本程序是健全的，因为它是单线程的。但 Rust 编译器按函数单独推理，无法做出这一假设。试着去掉 `unsafe`，看看编译器如何解释：从多个线程访问可变静态是未定义行为。
> - Rust 2024 edition 更进一步：默认情况下，通过引用访问可变静态是错误。
> - 使用可变静态很少是好主意，通常应改用内部可变性（interior mutability）。
> - 在底层 `no_std` 代码中偶有必要，例如实现堆分配器或与某些 C API 交互。此时应使用指针而非引用。

