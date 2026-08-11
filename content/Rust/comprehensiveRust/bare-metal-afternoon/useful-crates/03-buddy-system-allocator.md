+++
title = "2.3 `buddy_system_allocator`"
date = 2026-08-11T11:30:00+08:00
weight = 335
type = "docs"
description = "03-`buddy_system_allocator` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/useful-crates/buddy_system_allocator.html](https://google.github.io/comprehensive-rust/bare-metal/useful-crates/buddy_system_allocator.html)

# 2.3 `buddy_system_allocator`

[`buddy_system_allocator`][1] 是一个实现基本好友系统的 crate
分配器。它可以用来实现 [`GlobalAlloc`][3]（使用
[`LockedHeap`][2]）这样你就可以使用标准`alloc`板条箱（正如我们所看到的
[之前][4]），或用于分配其他地址空间（使用
[`FrameAllocator`][5]) 。例如，我们可能想要分配 MMIO 空间
PCI BAR：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use buddy_system_allocator::FrameAllocator;
use core::alloc::Layout;

fn main() {
    let mut allocator = FrameAllocator::<32>::new();
    allocator.add_frame(0x200_0000, 0x400_0000);

    let layout = Layout::from_size_align(0x100, 0x100).unwrap();
    let bar = allocator
        .alloc_aligned(layout)
        .expect("Failed to allocate 0x100 byte MMIO region");
    println!("Allocated 0x100 byte MMIO region at {:#x}", bar);
}
```

> - PCI BAR 的对齐方式始终等于其大小。
> - 运行该示例`cargo run`在下面
>   `src/bare-metal/useful-crates/allocator-example/`。 （它不会运行在
>   由于板条箱依赖性，游乐场。）


[1]: https://crates.io/crates/buddy_system_allocator
[2]: https://docs.rs/buddy_system_allocator/0.9.0/buddy_system_allocator/struct.LockedHeap.html
[3]: https://doc.rust-lang.org/core/alloc/trait.GlobalAlloc.html
[4]: ../alloc.md
[5]: https://docs.rs/buddy_system_allocator/0.9.0/buddy_system_allocator/struct.FrameAllocator.html
