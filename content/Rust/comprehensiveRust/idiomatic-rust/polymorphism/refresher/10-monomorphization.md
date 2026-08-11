+++
title = "4.1.10 单态化与二进制体积"
date = 2026-08-11T11:30:00+08:00
weight = 479
type = "docs"
description = "10-单态化与二进制体积 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/monomorphization.html](https://google.github.io/comprehensive-rust/idiomatic/polymorphism/refresher/monomorphization.html)

# 4.1.10 单态化与二进制体积

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn print_vec<T: std::fmt::Debug>(debug_vec: &Vec<T>) {
    for item in debug_vec {
        println!("{:?}", item);
    }
}

fn main() {
    let ints = vec![1u32, 2, 3];
    let floats = vec![1.1f32, 2.2, 3.3];

    // 实例一，&Vec<u32> -> ()
    print_vec(&ints);
    // 实例二，&Vec<f32> -> ()
    print_vec(&floats);
}
```

> - 带泛型的函数或类型的每一个实例，都会在编译期变成该函数的唯一、具体版本。运行时不存在泛型，只有具体类型。
>
> - 这带来很强的基线性能与优化空间，代价则是二进制体积与编译时间。
>
> - 缩减二进制体积与编译时间的办法很多，这里不展开。
>
> - 按需付费：单态化带来的体积增长，只发生在最终程序或动态库中实际用到的类型或该类型上的函数实例。
>
> - 何时需要关心：单态化影响编译时间与二进制体积。在浏览器 WebAssembly 或嵌入式开发等场景中，设计时可能需要留意泛型的使用。

