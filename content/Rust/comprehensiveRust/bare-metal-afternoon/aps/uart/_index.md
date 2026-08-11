+++
title = "1.4 我们来写一个UART驱动程序"
date = 2026-08-11T11:30:00+08:00
weight = 316
type = "docs"
description = "我们来写一个UART驱动程序 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/aps/uart.html](https://google.github.io/comprehensive-rust/bare-metal/aps/uart.html)

# 1.4 我们来写一个UART驱动程序

QEMU“虚拟”机器有一个 [PL011][1] UART，所以让我们为其编写一个驱动程序。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
const FLAG_REGISTER_OFFSET: usize = 0x18;
const FR_BUSY: u8 = 1 << 3;
const FR_TXFF: u8 = 1 << 5;

/// PL011 UART 的最小驱动程序。
#[derive(Debug)]
pub struct Uart {
    base_address: *mut u8,
}

impl Uart {
    /// 为 PL011 设备构造一个新的 UART 驱动程序实例
    /// 给定基地址。
    ///
    /// ＃ 安全
    ///
    /// 给定的基地址必须指向一个MMIO的8个控制寄存器
    ///PL011设备，必须映射到进程的地址空间
    /// 作为设备内存并且没有任何其他别名。
    pub unsafe fn new(base_address: *mut u8) -> Self {
        Self { base_address }
    }

    /// 将单个字节写入 UART。
    pub fn write_byte(&self, byte: u8) {
        // 等待，直到 TX 缓冲区中有空间。
        while self.read_flag_register() & FR_TXFF != 0 {}

        // 安全：我们知道基地址指向控件
        // 正确映射的 PL011 设备的寄存器。
        unsafe {
            // 写入 TX 缓冲区。
            self.base_address.write_volatile(byte);
        }

        // 等待 UART 不再繁忙。
        while self.read_flag_register() & FR_BUSY != 0 {}
    }

    fn read_flag_register(&self) -> u8 {
        // 安全：我们知道基地址指向控件
        // 正确映射的 PL011 设备的寄存器。
        unsafe { self.base_address.add(FLAG_REGISTER_OFFSET).read_volatile() }
    }
}
```

> - 注意`Uart::new`不安全，而其他方法是安全的。这是
>   因为只要调用者`Uart::new`保证其安全
>   满足要求（即只有一个驱动程序实例
>   对于给定的 UART，并且没有其他别名其地址空间），那么它是
>   打电话总是安全的`write_byte`稍后因为我们可以假设必要的
>   前提条件。
> - 我们本来可以用相反的方式做到这一点（使`new`安全但是`write_byte`
>   不安全），但是使用起来会不太方便，因为每个地方都有
>   来电`write_byte`需要考虑安全性
> - 这是编写不安全代码的安全包装器的常见模式：移动
>   从大量地方到较小地方的健全性举证责任
>   地点的数量。


[1]: https://developer.arm.com/documentation/ddi0183/g
