+++
title = "5.2.4 已记录的安全前置条件"
date = 2026-08-11T11:30:00+08:00
weight = 531
type = "docs"
description = "04-已记录的安全前置条件 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/copying-memory/documented-safety-preconditions.html](https://google.github.io/comprehensive-rust/unsafe-deep-dive/rules-of-the-game/copying-memory/documented-safety-preconditions.html)

# 5.2.4 已记录的安全前置条件

```rust
// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// ...
///
/// # 安全
///
/// 此函数很容易触发未定义行为。请确保：
///
///  - `source` 指针非 null 且非悬垂
///  - `source` 数据在其内存分配范围内以 null 字节结尾
///  - `source` 数据未被释放（其生命周期不变量得以保持）
///  - `source` 数据包含的字节数少于 `isize::MAX`
pub unsafe fn copy(dest: &mut [u8], source: *const u8) {
    let source = {
        let mut len = 0;

        let mut end = source;
        // SAFETY：调用方提供了非 null 指针
        while unsafe { *end != 0 } {
            len += 1;
            // SAFETY：调用方提供的数据长度 < isize::MAX
            end = unsafe { end.add(1) };
        }

        // SAFETY：调用方满足生命周期与别名要求
        unsafe { std::slice::from_raw_parts(source, len + 1) }
    };

    for (dest, src) in dest.iter_mut().zip(source) {
        *dest = *src;
    }
}

fn main() {
    let a = [114, 117, 115, 116].as_ptr();
    let b = &mut [82, 85, 83, 84, 0];

    println!("{}", String::from_utf8_lossy(b));
    unsafe {
        copy(b, a);
    }
    println!("{}", String::from_utf8_lossy(b));
}
```

> 与之前版本的变更：
>
> - `copy` 标记为 `unsafe`
> - 安全前置条件已记录在文档中
> - 行内 SAFETY 注释
>
> 当安全前置条件及其内部的 `unsafe` 块都有文档说明时，不安全函数才是健全的。
>
> `main` 中需要修正。
>
> - `a` 不满足 `copy` 的一项前置条件（`source` 数据在其内存分配范围内以 null 字节结尾）
> - 需要 SAFETY 注释

