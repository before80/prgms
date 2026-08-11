+++
title = "3.2.7 作用域 Guard"
date = 2026-08-11T11:30:00+08:00
weight = 437
type = "docs"
description = "07-作用域 Guard — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/raii/scope_guard.html](https://google.github.io/comprehensive-rust/idiomatic/leveraging-the-type-system/raii/scope_guard.html)

# 3.2.7 作用域 Guard

作用域 guard（scope guard）利用 `Drop` trait，在作用域退出时自动运行清理代码，即使在展开期间也是如此。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use scopeguard::{ScopeGuard, guard};
use std::fs::{self, File};
use std::io::Write;

fn download_successful() -> bool {
    // [...]
    true
}

fn main() {
    let path = "download.tmp";
    let mut file = File::create(path).expect("cannot create temporary file");

    // 创建文件后立即设置清理
    let cleanup = guard(path, |path| {
        println!("download failed, deleting: {:?}", path);
        let _ = fs::remove_file(path);
    });

    writeln!(file, "partial data...").unwrap();

    if download_successful() {
        // 下载成功，保留文件
        let path = ScopeGuard::into_inner(cleanup);
        println!("Download '{path}' complete!");
    }
    // 否则，guard 会运行并删除文件
}
```

> - 本示例建模下载工作流。我们先创建临时文件，再用作用域 guard 确保下载失败时删除该文件。
>
> - `scopeguard` crate 让你可以方便地定义一次性的、基于 `Drop` 的清理，而无需定义带自定义 `Drop` 实现的自定义类型。
>
> - Guard 在创建文件后立即创建，因此即使 `writeln!()` 失败，文件仍会被清理。这个顺序对正确性至关重要。
>
> - `guard()` 创建一个 `ScopeGuard` 实例。它接受用户定义的值（本例中是 `path`）以及稍后接收该值的清理闭包。
>
> - 除非用 `ScopeGuard::into_inner` **拆除**（取出值，使 guard 在 drop 时什么也不做），否则 guard 的闭包会在作用域退出时运行。在成功路径上，我们调用 `into_inner`，这样 guard 就不会删除文件。
>
> - 作用域 guard 类似于 Go 中的 `defer` 特性。
>
> - 此模式非常适合「失败时清理」场景：默认应运行清理，除非显式走成功路径。
>
> - 当你无法控制资源对象的清理策略时，此模式也很有用。本例中，`File::drop()` 会关闭文件但不会删除它。
>
> - `scopeguard` crate 还通过
>   [`Strategy`](https://docs.rs/scopeguard/latest/scopeguard/trait.Strategy.html)
>   trait 支持清理策略。你可以选择仅在展开时、或仅在成功时运行 guard，而不仅是总是运行。

