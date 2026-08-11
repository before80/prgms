+++
title = "4.2 裸金属生锈下午"
date = 2026-08-11T11:30:00+08:00
weight = 342
type = "docs"
description = "02-裸金属生锈下午 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/exercises/bare-metal/solutions-afternoon.html](https://google.github.io/comprehensive-rust/exercises/bare-metal/solutions-afternoon.html)

# 4.2 裸金属生锈下午

## 实时时钟驱动程序

（[返回练习](rtc.md)）

_main.rs_：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#![no_main]
#![no_std]

mod exceptions;
mod logger;
mod pl031;

use crate::pl031::Rtc;
use arm_gic::{IntId, Trigger, irq_enable, wfi};
use chrono::{TimeZone, Utc};
use core::hint::spin_loop;
use aarch64_paging::descriptor::El1Attributes;
use aarch64_rt::{InitialPagetable, entry, initial_pagetable};
use arm_gic::gicv3::registers::{Gicd, GicrSgi};
use arm_gic::gicv3::{GicCpuInterface, GicV3};
use arm_pl011_uart::{PL011Registers, Uart};
use core::panic::PanicInfo;
use core::ptr::NonNull;
use log::{LevelFilter, error, info, trace};
use safe_mmio::UniqueMmioPointer;
use smccc::Hvc;
use smccc::psci::system_off;

/// GICv3 的基地址。
const GICD_BASE_ADDRESS: NonNull<Gicd> = NonNull::new(0x800_0000 as _).unwrap();
const GICR_BASE_ADDRESS: NonNull<GicrSgi> = NonNull::new(0x80A_0000 as _).unwrap();

/// 主 PL011 UART 的基地址。
const PL011_BASE_ADDRESS: NonNull<PL011Registers> =
    NonNull::new(0x900_0000 as _).unwrap();

/// 用于初始标识映射中的设备内存的属性。
const DEVICE_ATTRIBUTES: El1Attributes = El1Attributes::VALID
    .union(El1Attributes::ATTRIBUTE_INDEX_0)
    .union(El1Attributes::ACCESSED)
    .union(El1Attributes::UXN);

/// 用于初始标识映射中的普通内存的属性。
const MEMORY_ATTRIBUTES: El1Attributes = El1Attributes::VALID
    .union(El1Attributes::ATTRIBUTE_INDEX_1)
    .union(El1Attributes::INNER_SHAREABLE)
    .union(El1Attributes::ACCESSED)
    .union(El1Attributes::NON_GLOBAL);

initial_pagetable!({
    let mut idmap = [0; 512];
    // 1 GiB 设备内存。
    idmap[0] = DEVICE_ATTRIBUTES.bits();
    // 1 GiB 普通内存。
    idmap[1] = MEMORY_ATTRIBUTES.bits() | 0x40000000;
    // 另外 1 GiB 设备内存从 256 GiB 开始。
    idmap[256] = DEVICE_ATTRIBUTES.bits() | 0x4000000000;
    InitialPagetable(idmap)
});

/// PL031 RTC 的基地址。
const PL031_BASE_ADDRESS: NonNull<pl031::Registers> =
    NonNull::new(0x901_0000 as _).unwrap();
/// PL031 RTC 使用的 IRQ。
const PL031_IRQ: IntId = IntId::spi(2);

entry!(main);
fn main(x0: u64, x1: u64, x2: u64, x3: u64) -> ! {
    // 安全：`PL011_BASE_ADDRESS`是 PL011 设备的基地址，并且
    // 没有其他东西可以访问该地址范围。
    let uart = unsafe { Uart::new(UniqueMmioPointer::new(PL011_BASE_ADDRESS)) };
    logger::init(uart, LevelFilter::Trace).unwrap();

    info!("main({:#x}, {:#x}, {:#x}, {:#x})", x0, x1, x2, x3);

    // 安全：`GICD_BASE_ADDRESS`和`GICR_BASE_ADDRESS`是基础
    // 分别是 GICv3 分发器和再分发器的地址，以及
    // 没有其他东西可以访问这些地址范围。
    let mut gic = unsafe {
        GicV3::new(
            UniqueMmioPointer::new(GICD_BASE_ADDRESS),
            GICR_BASE_ADDRESS,
            1,
            false,
        )
    };
    gic.setup(0);
    // ANCHOR_END：主要

    // 安全：`PL031_BASE_ADDRESS`是 PL031 设备的基地址，并且
    // 没有其他东西可以访问该地址范围。
    let mut rtc = unsafe { Rtc::new(UniqueMmioPointer::new(PL031_BASE_ADDRESS)) };
    let timestamp = rtc.read();
    let time = Utc.timestamp_opt(timestamp.into(), 0).unwrap();
    info!("RTC: {time}");

    GicCpuInterface::set_priority_mask(0xff);
    gic.set_interrupt_priority(PL031_IRQ, None, 0x80).unwrap();
    gic.set_trigger(PL031_IRQ, None, Trigger::Level).unwrap();
    irq_enable();
    gic.enable_interrupt(PL031_IRQ, None, true).unwrap();

    // 等待 3 秒钟，不要中断。
    let target = timestamp + 3;
    rtc.set_match(target);
    info!("Waiting for {}", Utc.timestamp_opt(target.into(), 0).unwrap());
    trace!(
        "matched={}, interrupt_pending={}",
        rtc.matched(),
        rtc.interrupt_pending()
    );
    while !rtc.matched() {
        spin_loop();
    }
    trace!(
        "matched={}, interrupt_pending={}",
        rtc.matched(),
        rtc.interrupt_pending()
    );
    info!("Finished waiting");

    // 再等待 3 秒以获得中断。
    let target = timestamp + 6;
    info!("Waiting for {}", Utc.timestamp_opt(target.into(), 0).unwrap());
    rtc.set_match(target);
    rtc.clear_interrupt();
    rtc.enable_interrupt(true);
    trace!(
        "matched={}, interrupt_pending={}",
        rtc.matched(),
        rtc.interrupt_pending()
    );
    while !rtc.interrupt_pending() {
        wfi();
    }
    trace!(
        "matched={}, interrupt_pending={}",
        rtc.matched(),
        rtc.interrupt_pending()
    );
    info!("Finished waiting");

    // 锚点：main_end
    system_off::<Hvc>().unwrap();
    panic!("system_off returned");
}

#[panic_handler]
fn panic(info: &PanicInfo) -> ! {
    error!("{info}");
    system_off::<Hvc>().unwrap();
    loop {}
}
```

_pl031.rs_：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#[repr(C, align(4))]
pub struct Registers {
    /// 数据寄存器
    dr: ReadPure<u32>,
    /// 匹配寄存器
    mr: ReadPureWrite<u32>,
    /// 加载寄存器
    lr: ReadPureWrite<u32>,
    /// 控制寄存器
    cr: ReadPureWrite<u8>,
    _reserved0: [u8; 3],
    /// 中断屏蔽设置或清除寄存器
    imsc: ReadPureWrite<u8>,
    _reserved1: [u8; 3],
    /// 原始中断状态
    ris: ReadPure<u8>,
    _reserved2: [u8; 3],
    /// 屏蔽中断状态
    mis: ReadPure<u8>,
    _reserved3: [u8; 3],
    /// 中断清除寄存器
    icr: WriteOnly<u8>,
    _reserved4: [u8; 3],
}

/// PL031 实时时钟的驱动程序。
#[derive(Debug)]
pub struct Rtc<'a> {
    registers: UniqueMmioPointer<'a, Registers>,
}

impl<'a> Rtc<'a> {
    /// 为 PL031 设备构造 RTC 驱动程序的新实例
    /// 给定的一组寄存器。
    pub fn new(registers: UniqueMmioPointer<'a, Registers>) -> Self {
        Self { registers }
    }

    /// 读取当前 RTC 值。
    pub fn read(&self) -> u32 {
        field_shared!(self.registers, dr).read()
    }

    /// 写入匹配值。当 RTC 值与此匹配时，就会产生中断
    /// 将被生成（如果已启用）。
    pub fn set_match(&mut self, value: u32) {
        field!(self.registers, mr).write(value);
    }

    /// 返回匹配寄存器是否与RTC值匹配，无论是否
    /// 中断已启用。
    pub fn matched(&self) -> bool {
        let ris = field_shared!(self.registers, ris).read();
        (ris & 0x01) != 0
    }

    /// 返回当前是否有待处理的中断。
    ///
    /// 这应该是真的当且仅当`matched`返回 true 并且
    /// 中断被屏蔽。
    pub fn interrupt_pending(&self) -> bool {
        let mis = field_shared!(self.registers, mis).read();
        (mis & 0x01) != 0
    }

    /// 设置或清除中断屏蔽。
    ///
    /// 当掩码为真时，中断被使能；当它为假时
    /// 中断被禁用。
    pub fn enable_interrupt(&mut self, mask: bool) {
        let imsc = if mask { 0x01 } else { 0x00 };
        field!(self.registers, imsc).write(imsc);
    }

    /// 清除挂起的中断（如果有）。
    pub fn clear_interrupt(&mut self) {
        field!(self.registers, icr).write(0x01);
    }
}
```
