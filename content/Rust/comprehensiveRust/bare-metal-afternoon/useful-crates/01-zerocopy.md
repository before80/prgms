+++
title = "2.1 `zerocopy`"
date = 2026-08-11T11:30:00+08:00
weight = 333
type = "docs"
description = "01-`zerocopy` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/useful-crates/zerocopy.html](https://google.github.io/comprehensive-rust/bare-metal/useful-crates/zerocopy.html)

# 2.1 `zerocopy`

这 [`zerocopy`][1] crate（来自 Fuchsia）提供安全的特征和宏
在字节序列和其他类型之间进行转换。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use zerocopy::{Immutable, IntoBytes};

#[repr(u32)]
#[derive(Debug, Default, Immutable, IntoBytes)]
enum RequestType {
    #[default]
    In = 0,
    Out = 1,
    Flush = 4,
}

#[repr(C)]
#[derive(Debug, Default, Immutable, IntoBytes)]
struct VirtioBlockRequest {
    request_type: RequestType,
    reserved: u32,
    sector: u64,
}

fn main() {
    let request = VirtioBlockRequest {
        request_type: RequestType::Flush,
        sector: 42,
        ..Default::default()
    };

    assert_eq!(
        request.as_bytes(),
        &[4, 0, 0, 0, 0, 0, 0, 0, 42, 0, 0, 0, 0, 0, 0, 0]
    );
}
```

这不适合 MMIO（因为它不使用易失性读取和写入），但是
对于处理与硬件共享的结构非常有用，例如通过 DMA，或
通过一些外部接口发送。

> - `FromBytes`可以针对任何字节模式都有效的类型来实现，
>   因此可以安全地从不受信任的字节序列进行转换。
> - 尝试推导`FromBytes`对于这些类型会失败，因为
>   `RequestType`不使用所有可能的 u32 值作为判别式，因此并非所有
>   字节模式有效。
> - `zerocopy::byteorder`具有字节顺序感知数字原语的类型。
> - 运行该示例`cargo run`在下面
>   `src/bare-metal/useful-crates/zerocopy-example/`。 （它不会运行在
>   由于板条箱依赖性，游乐场。）


[1]: https://docs.rs/zerocopy/
