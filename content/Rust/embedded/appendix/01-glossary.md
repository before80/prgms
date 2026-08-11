+++
title = "12-附录 A：术语表"
date = 2026-08-01T10:38:00+08:00
weight = 162
type = "docs"
description = "附录 A：术语表"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 附录 A：术语表 {#appendix-a-glossary}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/appendix/glossary.html](https://doc.rust-lang.org/stable/embedded-book/appendix/glossary.html)


嵌入式生态充满了使用各自术语与缩写的不同协议、硬件组件以及厂商特定事物。本术语表尝试列出它们，并给出便于进一步理解的指引。

### BSP

板级支持包（Board Support Crate）为特定开发板提供已配置的高层次接口。它通常依赖 [HAL](#hal) crate。
更详细的说明见[内存映射寄存器页面](../start/03-memory-mapped-registers/)，
或观看[本视频](https://youtu.be/vLYit_HHPaY)以获得更广的概览。

### FPU

浮点运算单元（Floating-point Unit）。只对浮点数执行运算的「数学处理器」。

### HAL

硬件抽象层（Hardware Abstraction Layer）crate 为微控制器的功能与外设提供对开发者友好的接口。它通常实现在 [外设访问 crate（PAC）](#pac) 之上。
它也可能实现 [`embedded-hal`](https://crates.io/crates/embedded-hal) crate 中的 trait。
更详细的说明见[内存映射寄存器页面](../start/03-memory-mapped-registers/)，
或观看[本视频](https://youtu.be/vLYit_HHPaY)以获得更广的概览。

### I2C

有时写作 `I²C` 或 Inter-IC。这是一种面向单个集成电路内部硬件通信的协议。更多细节见[此处][i2c]

[i2c]: https://en.wikipedia.org/wiki/I2c

### PAC

外设访问 crate（Peripheral Access Crate）提供对微控制器外设的访问。它是较低层的 crate 之一，通常直接从所提供的 [SVD](#svd) 生成，常用 [svd2rust](https://github.com/rust-embedded/svd2rust/)。[硬件抽象层](#hal)通常会依赖该 crate。
更详细的说明见[内存映射寄存器页面](../start/03-memory-mapped-registers/)，
或观看[本视频](https://youtu.be/vLYit_HHPaY)以获得更广的概览。

### SPI

串行外设接口（Serial Peripheral Interface）。更多信息见[此处][spi]。

[spi]: https://en.wikipedia.org/wiki/Serial_peripheral_interface

### SVD

系统视图描述（System View Description）是一种 XML 文件格式，用于描述微控制器设备的程序员视图。你可以在
[ARM CMSIS 文档站点](https://www.keil.com/pack/doc/CMSIS/SVD/html/index.html)了解更多。

### UART

通用异步收发器（Universal asynchronous receiver-transmitter）。更多信息见[此处][uart]。

[uart]: https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter

### USART

通用同步异步收发器（Universal synchronous and asynchronous receiver-transmitter）。更多信息见[此处][usart]。

[usart]: https://en.wikipedia.org/wiki/Universal_synchronous_and_asynchronous_receiver-transmitter
