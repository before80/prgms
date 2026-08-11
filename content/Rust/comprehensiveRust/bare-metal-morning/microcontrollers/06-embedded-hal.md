+++
title = "3.6 `embedded-hal`"
date = 2026-08-11T11:30:00+08:00
weight = 304
type = "docs"
description = "06-`embedded-hal` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/microcontrollers/embedded-hal.html](https://google.github.io/comprehensive-rust/bare-metal/microcontrollers/embedded-hal.html)

# 3.6 `embedded-hal`

[`embedded-hal`] crate 提供覆盖常见微控制器外设的一组 trait：

- GPIO
- PWM
- 延时定时器
- I2C 与 SPI 总线及设备

字节流（如 UART）、CAN 总线与 RNG 的类似 trait 分别拆到 [`embedded-io`]、[`embedded-can`] 与 [`rand_core`] 中。

其他 crate 再基于这些 trait 实现[驱动][drivers]，例如加速度计驱动可能需要一个 I2C 或 SPI 设备实例。

> - 这些 trait 覆盖外设的*使用*，但不覆盖初始化或配置，因为初始化与配置高度依赖平台。
> - 许多微控制器都有实现，也有树莓派上 Linux 等其他平台。
> - [`embedded-hal-async`] 提供这些 trait 的 async 版本。
> - [`embedded-hal-nb`] 基于 [`nb`] crate，提供另一种非阻塞 I/O 方式。


[drivers]: https://github.com/rust-embedded/awesome-embedded-rust#driver-crates
[`embedded-can`]: https://crates.io/crates/embedded-can
[`embedded-hal`]: https://crates.io/crates/embedded-hal
[`embedded-hal-async`]: https://crates.io/crates/embedded-hal-async
[`embedded-hal-nb`]: https://crates.io/crates/embedded-hal-nb
[`embedded-io`]: https://crates.io/crates/embedded-io
[`nb`]: https://crates.io/crates/nb
[`rand_core`]: https://crates.io/crates/rand_core
