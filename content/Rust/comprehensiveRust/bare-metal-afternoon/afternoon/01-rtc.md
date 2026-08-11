+++
title = "4.1 RTC 驱动"
date = 2026-08-11T11:30:00+08:00
weight = 341
type = "docs"
description = "01-RTC 驱动 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/exercises/bare-metal/rtc.html](https://google.github.io/comprehensive-rust/exercises/bare-metal/rtc.html)

# 4.1 RTC 驱动

QEMU aarch64 virt 机器在 0x9010000 有一个 [PL031][1] 实时时钟。本练习中，你应为其编写驱动。

1. 用它把当前时间打印到串口控制台。可用 [`chrono`][2] crate 做日期/时间格式化。
2. 使用 match 寄存器与原始中断状态，忙等到给定时间（例如未来 3 秒）。（在循环内调用 [`core::hint::spin_loop`][3]。）
3. _若有时间可扩展：_启用并处理 RTC match 产生的中断。可用 [`arm-gic`][4] crate 中的驱动配置 Arm Generic Interrupt Controller。
   - 使用 RTC 中断，它接到 GIC 上为 `IntId::spi(2)`。
   - 启用中断后，可通过 `arm_gic::wfi()` 让核心休眠，直到收到中断。

下载[练习模板](../../comprehensive-rust-exercises.zip)，在 `rtc` 目录中查看下列文件。

_src/main.rs_：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
#![no_main]
#![no_std]

mod exceptions;
mod logger;

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

/// 初始 identity map 中设备内存使用的属性。
const DEVICE_ATTRIBUTES: El1Attributes = El1Attributes::VALID
    .union(El1Attributes::ATTRIBUTE_INDEX_0)
    .union(El1Attributes::ACCESSED)
    .union(El1Attributes::UXN);

/// 初始 identity map 中普通内存使用的属性。
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
    // 从 256 GiB 起另有 1 GiB 设备内存。
    idmap[256] = DEVICE_ATTRIBUTES.bits() | 0x4000000000;
    InitialPagetable(idmap)
});

entry!(main);
fn main(x0: u64, x1: u64, x2: u64, x3: u64) -> ! {
    // SAFETY: `PL011_BASE_ADDRESS` 是 PL011 设备的基地址，且没有其他代码访问该地址范围。
    let uart = unsafe { Uart::new(UniqueMmioPointer::new(PL011_BASE_ADDRESS)) };
    logger::init(uart, LevelFilter::Trace).unwrap();

    info!("main({:#x}, {:#x}, {:#x}, {:#x})", x0, x1, x2, x3);

    // SAFETY: `GICD_BASE_ADDRESS` 与 `GICR_BASE_ADDRESS` 分别是 GICv3 distributor 与 redistributor 的基地址，且没有其他代码访问这些地址范围。
    let mut gic = unsafe {
        GicV3::new(
            UniqueMmioPointer::new(GICD_BASE_ADDRESS),
            GICR_BASE_ADDRESS,
            1,
            false,
        )
    };
    gic.setup(0);

    // TODO：创建 RTC 驱动实例并打印当前时间。

    // TODO：等待 3 秒。

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

_src/exceptions.rs_（通常只需在练习第 3 部分修改此文件）：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use aarch64_rt::{ExceptionHandlers, RegisterStateRef, exception_handlers};
use arm_gic::InterruptGroup;
use arm_gic::gicv3::GicCpuInterface;
use log::{error, info, trace};
use smccc::Hvc;
use smccc::psci::system_off;

struct Handlers;

impl ExceptionHandlers for Handlers {
    extern "C" fn sync_current(_state: RegisterStateRef) {
        error!("sync_current");
        system_off::<Hvc>().unwrap();
    }

    extern "C" fn irq_current(_state: RegisterStateRef) {
        trace!("irq_current");
        let intid =
            GicCpuInterface::get_and_acknowledge_interrupt(InterruptGroup::Group1)
                .expect("No pending interrupt");
        info!("IRQ {intid:?}");
    }

    extern "C" fn fiq_current(_state: RegisterStateRef) {
        error!("fiq_current");
        system_off::<Hvc>().unwrap();
    }

    extern "C" fn serror_current(_state: RegisterStateRef) {
        error!("serror_current");
        system_off::<Hvc>().unwrap();
    }

    extern "C" fn sync_lower(_state: RegisterStateRef) {
        error!("sync_lower");
        system_off::<Hvc>().unwrap();
    }

    extern "C" fn irq_lower(_state: RegisterStateRef) {
        error!("irq_lower");
        system_off::<Hvc>().unwrap();
    }

    extern "C" fn fiq_lower(_state: RegisterStateRef) {
        error!("fiq_lower");
        system_off::<Hvc>().unwrap();
    }

    extern "C" fn serror_lower(_state: RegisterStateRef) {
        error!("serror_lower");
        system_off::<Hvc>().unwrap();
    }
}

exception_handlers!(Handlers);
```

_src/logger.rs_（通常无需修改）：

```rust
// Copyright 2023 Google LLC
// SPDX-License-Identifier: Apache-2.0
use arm_pl011_uart::Uart;
use core::fmt::Write;
use log::{LevelFilter, Log, Metadata, Record, SetLoggerError};
use spin::mutex::SpinMutex;

static LOGGER: Logger = Logger { uart: SpinMutex::new(None) };

struct Logger {
    uart: SpinMutex<Option<Uart<'static>>>,
}

impl Log for Logger {
    fn enabled(&self, _metadata: &Metadata) -> bool {
        true
    }

    fn log(&self, record: &Record) {
        writeln!(
            self.uart.lock().as_mut().unwrap(),
            "[{}] {}",
            record.level(),
            record.args()
        )
        .unwrap();
    }

    fn flush(&self) {}
}

/// 初始化 UART logger。
pub fn init(
    uart: Uart<'static>,
    max_level: LevelFilter,
) -> Result<(), SetLoggerError> {
    LOGGER.uart.lock().replace(uart);

    log::set_logger(&LOGGER)?;
    log::set_max_level(max_level);
    Ok(())
}
```

_Cargo.toml_（通常无需修改）：

```toml
[workspace]

[package]
name = "rtc"
version = "0.1.0"
edition = "2024"
publish = false

[dependencies]
aarch64-paging = { version = "0.12.1", default-features = false }
aarch64-rt = "0.4.3"
arm-gic = "0.8.1"
arm-pl011-uart = "0.5.0"
bitflags = "2.11.1"
chrono = { version = "0.4.44", default-features = false }
log = "0.4.30"
safe-mmio = "0.3.0"
smccc = "0.2.3"
spin = "0.12.0"
zerocopy = "0.8.50"
```

_build.rs_（通常无需修改）：

```rust
// Copyright 2025 Google LLC
// SPDX-License-Identifier: Apache-2.0
fn main() {
    println!("cargo:rustc-link-arg=-Timage.ld");
    println!("cargo:rustc-link-arg=-Tmemory.ld");
    println!("cargo:rerun-if-changed=memory.ld");
}
```

_memory.ld_（通常无需修改）：

```ld
/*
 * Copyright 2023 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

MEMORY
{
	image : ORIGIN = 0x40080000, LENGTH = 2M
}
```

_Makefile_（通常无需修改）：

```makefile
# Copyright 2023 Google LLC
# SPDX-License-Identifier: Apache-2.0

.PHONY: build qemu_minimal qemu qemu_logger

all: rtc.bin

build:
	cargo build

rtc.bin: build
	cargo objcopy -- -O binary $@

qemu: rtc.bin
	qemu-system-aarch64 -machine virt,gic-version=3 -cpu max -serial mon:stdio -display none -kernel $< -s

clean:
	cargo clean
	rm -f *.bin
```

_.cargo/config.toml_（通常无需修改）：

```toml
[build]
target = "aarch64-unknown-none"
```

在 QEMU 中用 `make qemu` 运行代码。

[1]: https://developer.arm.com/documentation/ddi0224/c
[2]: https://crates.io/crates/chrono
[3]: https://doc.rust-lang.org/core/hint/fn.spin_loop.html
[4]: https://docs.rs/arm-gic/
