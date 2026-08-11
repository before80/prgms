+++
title = "5.2.1 Safe Rust（安全 Rust）"
date = 2026-08-11T11:30:00+08:00
weight = 528
type = "docs"
description = "01-Safe Rust（安全 Rust） — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/copying-memory/safe.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/copying-memory/safe.html)

# 5.2.1 Safe Rust（安全 Rust）

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
pub fn copy(dest: &mut [u8], source: &[u8]) {
    for (dest, src) in dest.iter_mut().zip(source) {
        *dest = *src;
    }
}

fn main() {
    let a = &[114, 117, 115, 116];
    let b = &mut [82, 85, 83, 84];

    println!("{}", String::from_utf8_lossy(b));
    copy(b, a);
    println!("{}", String::from_utf8_lossy(b));
}
```

> 「该实现只使用了 Safe Rust。
>
> 我们能从中得出什么？
>
> 「当用 Safe Rust 实现时，对于所有可能的输入参数，`copy` 都不可能触发内存安全问题。」
>
> 「例如，通过 Rust 的迭代器，我们可以确保永远不会触发与直接操作指针相关的问题，比如需要空指针检查或边界检查。」
>
> 提问：「还能想到其他例子吗？」
>
> - 没有别名（aliasing）问题
> - 不可能出现悬垂指针
> - 对齐（alignment）始终正确
> - 不会意外读取未初始化的内存
>
> 「我们可以说 `copy` 函数是 _健全的_，因为 Rust 确保所有安全前置条件都得到满足。」
>
> 「从程序员的角度看，由于该函数用 Safe Rust 实现，可以认为它没有安全前置条件。」
>
> 「这并不意味着 `copy` 总能满足调用方的一切期望。如果 `dest` 切片空间不足，数据就不会被完整复制过去。」

