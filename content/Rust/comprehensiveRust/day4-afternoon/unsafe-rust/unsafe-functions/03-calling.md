+++
title = "3.5.3 调用 Unsafe 函数"
date = 2026-08-11T11:30:00+08:00
weight = 204
type = "docs"
description = "03-调用 Unsafe 函数 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-rust/unsafe-functions/calling.html](https://google.github.io/comprehensive-rust/unsafe-rust/unsafe-functions/calling.html)

# 3.5.3 调用 Unsafe 函数

未能满足安全要求会破坏内存安全！

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[derive(Debug)]
#[repr(C)]
struct KeyPair {
    pk: [u16; 4], // 8 bytes
    sk: [u16; 4], // 8 bytes
}

const PK_BYTE_LEN: usize = 8;

fn log_public_key(pk_ptr: *const u16) {
    let pk: &[u16] = unsafe { std::slice::from_raw_parts(pk_ptr, PK_BYTE_LEN) };
    println!("{pk:?}");
}

fn main() {
    let key_pair = KeyPair { pk: [1, 2, 3, 4], sk: [0, 0, 42, 0] };
    log_public_key(key_pair.pk.as_ptr());
}
```

请始终为每个 `unsafe` 块附上 safety 注释，解释为何该代码实际上是安全的。本例缺少 safety 注释，并且是不健全（unsound）的。

> <summary>讲师备注</summary>
>
> 要点：
>
> - `slice::from_raw_parts` 的第二个参数是**元素**个数，不是字节数！本例通过读越一个数组的末尾进入另一个数组，演示了意外行为。
> - 这是未定义行为，因为我们读越了导出该指针的数组末尾。
> - `log_public_key` 应当是 unsafe 的，因为 `pk_ptr` 必须满足某些前提才能避免未定义行为。一个可能造成未定义行为的安全函数被称为 `unsound`（不健全）。它的 safety 文档该写什么？
> - 标准库包含许多底层 unsafe 函数。可能的话优先使用安全替代方案！
> - 若把 unsafe 函数用作优化手段，务必加上基准测试来证明收益。

