+++
title = "03-外设"
date = 2026-08-01T10:38:00+08:00
weight = 55
type = "docs"
description = "外设（Peripherals）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 外设 {#peripherals}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/peripherals/](https://doc.rust-lang.org/stable/embedded-book/peripherals/)


## 什么是外设？ {#what-are-peripherals}

大多数微控制器并不只有 CPU、RAM 或 Flash —— 硅片上还有一些区域，用于与微控制器之外的系统交互，并直接或间接地通过传感器、电机控制器，或显示屏、键盘等人机接口与现实世界交互。这些部件统称为外设（Peripherals）。

外设很有用，因为开发者可以把处理工作卸载给它们，而不必全部在软件里完成。就像桌面开发者会把图形处理卸载给显卡一样，嵌入式开发者也可以把部分任务交给外设，让 CPU 去做别的重要事情，或者什么都不做以节省功耗。

如果你看过上世纪七八十年代老式家用电脑的主板（其实昨天的桌面 PC 与今天的嵌入式系统也并不遥远），你会期望看到：

* 一块处理器
* 一块 RAM 芯片
* 一块 ROM 芯片
* 一块 I/O 控制器

RAM、ROM 和 I/O 控制器（该系统中的外设）会通过一系列称为「总线（bus）」的并行走线连接到处理器。总线携带地址信息，用来选择处理器想与总线上哪个设备通信，以及携带实际数据的数据总线。在嵌入式微控制器里，原理相同 —— 只是一切都封装在同一块硅片上。

不过，与通常提供 Vulkan、Metal 或 OpenGL 这类软件 API 的显卡不同，外设是通过硬件接口暴露给我们的微控制器的，并且被映射到一段内存上。

## 线性与真实内存空间 {#linear-and-real-memory-space}

在微控制器上，向某个任意地址写入数据，例如 `0x4000_0000` 或 `0x0000_0000`，也可能是完全合法的操作。

在桌面系统上，内存访问由 MMU（内存管理单元，Memory Management Unit）严格控制。该组件有两大职责：强制执行对内存区段的访问权限（防止一个进程读写另一进程的内存）；以及把物理内存段重新映射到软件使用的虚拟内存范围。微控制器通常没有 MMU，软件中只用真实的物理地址。

虽然 32 位微控制器拥有从 `0x0000_0000` 到 `0xFFFF_FFFF` 的真实线性地址空间，但它们一般只把其中几百 KB 用作实际内存。这留下了相当大的剩余地址空间。在前面的章节里，我们提到 RAM 位于地址 `0x2000_0000`。如果 RAM 长度为 64 KiB（即最大地址为 0xFFFF），那么地址 `0x2000_0000` 到 `0x2000_FFFF` 就对应我们的 RAM。当我们向位于 `0x2000_1234` 的变量写入时，内部会发生这样的事：某些逻辑检测到地址的高位部分（本例中为 0x2000），然后激活 RAM，使其作用于地址的低位部分（本例中为 0x1234）。在 Cortex-M 上，Flash ROM 还被映射到 `0x0000_0000`，一直到例如 `0x0007_FFFF`（若我们有 512 KiB Flash ROM）。微控制器设计者并没有忽略这两个区域之间的剩余空间，而是把外设接口映射到某些内存位置。最终看起来大致如下：

![](../assets/nrf52-memory-map.png)

[Nordic nRF52832 Datasheet (pdf)]

## 内存映射外设 {#memory-mapped-peripherals}

乍一看，与这些外设交互很简单 —— 把正确的数据写到正确的地址即可。例如，通过串口发送一个 32 位字，可以直接把该 32 位字写到某个内存地址。串口外设随后会接管并自动把数据发出去。

这些外设的配置方式类似。不是调用函数来配置外设，而是暴露出一块内存作为硬件 API。向 SPI 频率配置寄存器写入 `0x8000_0000`，SPI 端口就会以 8 Mbps 发送数据。向同一地址写入 `0x0200_0000`，SPI 端口就会以 125 Kbps 发送数据。这些配置寄存器看起来有点像这样：

![](../assets/nrf52-spi-frequency-register.png)

[Nordic nRF52832 Datasheet (pdf)]

无论使用何种语言 —— 汇编、C 还是 Rust —— 与硬件的交互都是通过这种接口完成的。

[Nordic nRF52832 Datasheet (pdf)]: http://infocenter.nordicsemi.com/pdf/nRF52832_PS_v1.1.pdf

## 本章其它页面 {#related-pages}

- [01-用 Rust 的第一次尝试](01-a-first-attempt-in-rust/)
- [02-借用检查器](02-the-borrow-checker/)
- [03-单例](03-singletons/)
