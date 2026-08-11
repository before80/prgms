+++
title = "1.3 MMIO 的易失性内存访问"
date = 2026-08-11T11:30:00+08:00
weight = 315
type = "docs"
description = "03-MMIO 的易失性内存访问 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/aps/mmio.html](https://google.github.io/comprehensive-rust/bare-metal/aps/mmio.html)

# 1.3 MMIO 的易失性内存访问

- 使用 [`pointer::read_volatile`] 和 [`pointer::write_volatile`]。
- 切勿保留对使用这些方法访问的位置的引用。锈
  可以随时读取（或写入，对于“&mut”）引用。
- 使用“&raw”获取结构体字段而不创建中间体
  参考。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
const SOME_DEVICE_REGISTER: *mut u64 = 0x800_0000 as _;
// 安全：某些设备映射到此地址。
unsafe {
    SOME_DEVICE_REGISTER.write_volatile(0xff);
    SOME_DEVICE_REGISTER.write_volatile(0x80);
    assert_eq!(SOME_DEVICE_REGISTER.read_volatile(), 0xaa);
}
```

[`指针::read_volatile`]: https://doc.rust-lang.org/stable/core/primitive.pointer.html#method.read_volatile
[`指针::write_volatile`]: https://doc.rust-lang.org/stable/core/primitive.pointer.html#method.write_volatile
[`addr_of!`]: https://doc.rust-lang.org/stable/core/ptr/macro.addr_of.html

> - 易失性访问：读或写操作可能会产生副作用，因此要防止
>   编译器或硬件对它们进行重新排序、复制或删除。
>   - 如果你先写然后读，例如通过可变引用，编译器可以
>     假设读取的值与刚刚写入的值相同，而不是
>     麻烦实际读取内存。
> - 一些现有的用于对硬件进行易失性访问的包确实保存了引用，但是
>   这是不健全的。只要存在引用，编译器就可以选择
>   取消引用它。
> - 使用“&raw”从指向结构的指针获取结构字段指针。
> - 为了与旧版本的 Rust 兼容，您可以使用 [`addr_of!`] 宏
>   反而。

