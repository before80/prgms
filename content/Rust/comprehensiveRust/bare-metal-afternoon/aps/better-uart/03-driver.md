+++
title = "1.5.3 司机"
date = 2026-08-11T11:30:00+08:00
weight = 322
type = "docs"
description = "03-司机 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/aps/better-uart/driver.html](https://google.github.io/comprehensive-rust/bare-metal/aps/better-uart/driver.html)

# 1.5.3 司机

现在让我们使用新的`Registers`我们的驱动程序中的结构体。

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
/// PL011 UART 的驱动程序。
#[derive(Debug)]
pub struct Uart {
    registers: *mut Registers,
}

impl Uart {
    /// 为 PL011 设备构建 UART 驱动程序的新实例
    /// 给定的一组寄存器。
    ///
    /// ＃ 安全
    ///
    /// 给定的指针必须指向PL011的8个MMIO控制寄存器
    ///device，必须映射到进程的地址空间
    ///设备内存并且没有任何其他别名。
    pub unsafe fn new(registers: *mut Registers) -> Self {
        Self { registers }
    }

    /// 将单个字节写入 UART。
    pub fn write_byte(&mut self, byte: u8) {
        // 等待，直到 TX 缓冲区中有空间。
        while self.read_flag_register().contains(Flags::TXFF) {}

        // 安全：我们知道 self.registers 指向控制寄存器
        // 已正确映射的 PL011 设备的。
        unsafe {
            // 写入 TX 缓冲区。
            (&raw mut (*self.registers).dr).write_volatile(byte.into());
        }

        // 等待 UART 不再繁忙。
        while self.read_flag_register().contains(Flags::BUSY) {}
    }

    /// 读取并返回一个待处理字节，或者`None`如果什么都没有
    /// 已收到。
    pub fn read_byte(&mut self) -> Option<u8> {
        if self.read_flag_register().contains(Flags::RXFE) {
            None
        } else {
            // 安全：我们知道 self.registers 指向控件
            // 正确映射的 PL011 设备的寄存器。
            let data = unsafe { (&raw const (*self.registers).dr).read_volatile() };
            // TODO：检查位 8-11 中的错误情况。
            Some(data as u8)
        }
    }

    fn read_flag_register(&self) -> Flags {
        // 安全：我们知道 self.registers 指向控制寄存器
        // 已正确映射的 PL011 设备的。
        unsafe { (&raw const (*self.registers).fr).read_volatile() }
    }
}
```

> - 注意使用`&raw const` / `&raw mut`获取指向各个字段的指针
>   而不创建中间引用，这是不合理的。
> - 该示例未包含在幻灯片中，因为它与
>   `safe-mmio`接下来的例子。您可以在 QEMU 中运行它`make qemu`在下面`src/bare-metal/aps/examples`如果你需要的话。

