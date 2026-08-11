+++
title = "2.2 `aarch64 分页`"
date = 2026-08-11T11:30:00+08:00
weight = 334
type = "docs"
description = "02-`aarch64 分页` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/useful-crates/aarch64-paging.html](https://google.github.io/comprehensive-rust/bare-metal/useful-crates/aarch64-paging.html)

# 2.2 `aarch64 分页`

[`aarch64-paging`][1] 包允许您根据
AArch64 虚拟内存系统架构。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use aarch64_paging::{
    idmap::IdMap,
    paging::{Attributes, MemoryRegion},
};

const ASID: usize = 1;
const ROOT_LEVEL: usize = 1;

// 创建具有标识映射的新页表。
let mut idmap = IdMap::new(ASID, ROOT_LEVEL);
// 将 2 MiB 内存区域映射为只读。
idmap.map_range(
    &MemoryRegion::new(0x80200000, 0x80400000),
    Attributes::NORMAL | Attributes::NON_GLOBAL | Attributes::READ_ONLY,
).unwrap();
// 设置`TTBR0_EL1`来激活页表。
idmap.activate();
```

> - 这在 Android 中用于[受保护的虚拟机固件][2]。
> - 单独运行这个示例没有简单的方法，因为它需要在真实的环境中运行
>   硬件或 QEMU 下。


[1]: https://crates.io/crates/aarch64-paging
[2]: https://cs.android.com/android/platform/superproject/main/+/main:packages/modules/Virtualization/guest/pvmfw/
