+++
title = "1.6.1 司机"
date = 2026-08-11T11:30:00+08:00
weight = 324
type = "docs"
description = "01-司机 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/aps/safemmio/driver.html](https://google.github.io/comprehensive-rust/bare-metal/aps/safemmio/driver.html)

# 1.6.1 司机

现在让我们使用新的`Registers`我们的驱动程序中的结构体。

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
use safe_mmio::{UniqueMmioPointer, field, field_shared};

/// PL011 UART 的驱动程序。
#[derive(Debug)]
pub struct Uart<'a> {
    registers: UniqueMmioPointer<'a, Registers>,
}

impl<'a> Uart<'a> {
    /// 为 PL011 设备构建 UART 驱动程序的新实例
    /// 给定的一组寄存器。
    pub fn new(registers: UniqueMmioPointer<'a, Registers>) -> Self {
        Self { registers }
    }

    /// 将单个字节写入 UART。
    pub fn write_byte(&mut self, byte: u8) {
        // 等待，直到 TX 缓冲区中有空间。
        while self.read_flag_register().contains(Flags::TXFF) {}

        // 写入 TX 缓冲区。
        field!(self.registers, dr).write(byte.into());

        // 等待 UART 不再繁忙。
        while self.read_flag_register().contains(Flags::BUSY) {}
    }

    /// 读取并返回一个待处理字节，或者`None`如果什么都没有
    /// 已收到。
    pub fn read_byte(&mut self) -> Option<u8> {
        if self.read_flag_register().contains(Flags::RXFE) {
            None
        } else {
            let data = field!(self.registers, dr).read();
            // TODO：检查位 8-11 中的错误情况。
            Some(data as u8)
        }
    }

    fn read_flag_register(&self) -> Flags {
        field_shared!(self.registers, fr).read()
    }
}
```

> - 驱动程序不再需要任何不安全的代码！
> - `UniqueMmioPointer`是指向 MMIO 设备的原始指针的包装器，或者
>   登记。来电者为`UniqueMmioPointer::new`承诺其有效并且
>   对于给定的生命周期是唯一的，因此它可以提供安全的方法来读取和
>   写入字段。
> - 注意`Uart::new`现在安全了；`UniqueMmioPointer::new`反而不安全。
> - 这些 MMIO 访问通常是一个包装器`read_volatile`和
>   `write_volatile`，尽管在 aarch64 上它们是在汇编中实现的
>   解决编译器可以发出阻止的指令的错误
>   MMIO 虚拟化。
> - 这`field!`和`field_shared!`内部使用宏`&raw mut`和
>   `&raw const`获取指向各个字段的指针而不创建
>   中间参考，这是不合理的。
> - `field!`需要一个可变引用`UniqueMmioPointer`，并返回一个
>   `UniqueMmioPointer`允许有副作用的读取和写入。
> - `field_shared!`使用对任一的共享引用`UniqueMmioPointer`
>   或一个`SharedMmioPointer`。它返回一个`SharedMmioPointer`只允许
>   纯读。

