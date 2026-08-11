+++
title = "4.6 静态变量"
date = 2026-08-11T11:30:00+08:00
weight = 60
type = "docs"
description = "06-静态变量 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/user-defined-types/static.html](https://google.github.io/comprehensive-rust/user-defined-types/static.html)

# 4.6 静态变量

静态变量在整个程序执行期间都存在，因此不会移动：

```rust
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
static BANNER: &str = "Welcome to RustOS 3.14";

fn main() {
    println!("{BANNER}");
}
```

如 [Rust RFC Book][1] 所述，静态变量在使用时不会被内联，而是有实际的关联内存位置。这对 unsafe 与嵌入式代码很有用，且该变量贯穿整个程序执行期。当全局作用域的值没有需要对象身份（object identity）的理由时，通常更推荐使用 `const`。

> - `static` 类似于 C++ 中的可变全局变量。
> - `static` 提供对象身份：内存中的地址，以及如 `Mutex<T>` 等具有内部可变性（interior mutability）的类型所需的状态。
>
> # 延伸阅读
>
> 因为 `static` 变量可从任意线程访问，它们必须是 `Sync` 的。
> 内部可变性可通过
> [`Mutex`](https://doc.rust-lang.org/std/sync/struct.Mutex.html)、原子类型或类似机制实现。
>
> 常见做法是在 `static` 中使用 `OnceLock`，以支持首次使用时初始化。`OnceCell` 不是 `Sync`，因此不能用在这种场景。
>
> 线程局部数据可用宏 `std::thread_local` 创建。


[1]: https://rust-lang.github.io/rfcs/0246-const-vs-static.html
