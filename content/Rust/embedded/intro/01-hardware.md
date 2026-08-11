+++
title = "01-硬件"
date = 2026-08-01T10:38:00+08:00
weight = 12
type = "docs"
description = "硬件（Hardware）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 硬件 {#meet-your-hardware}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/intro/hardware.html](https://doc.rust-lang.org/stable/embedded-book/intro/hardware.html)


让我们先熟悉一下将要使用的硬件。

## STM32F3DISCOVERY（简称 “F3”） {#stm32f3discovery-the-f3}

<p align="center">
<img title="F3 开发板" src="../assets/f3.jpg">
</p>

这块板子包含什么？

- 一颗 [STM32F303VCT6](https://www.st.com/en/microcontrollers/stm32f303vc.html) 微控制器。该微控制器具有：
  - 单核 ARM Cortex-M4F 处理器，硬件支持单精度浮点运算，最高时钟频率 72 MHz。

  - 256 KiB “Flash” 存储器。（1 KiB = 10**24** 字节）

  - 48 KiB RAM。

  - 多种集成外设，如定时器、I2C、SPI 与 USART。

  - 通用输入输出（GPIO）及其它类型引脚，可通过板子两侧的两排排针访问。

  - 一个 Mini-USB 接口，可通过标有 “USB USER” 的 USB 端口访问。

- 作为 [LSM303DLHC](https://www.st.com/en/mems-and-sensors/lsm303dlhc.html) 芯片一部分的[加速度计（accelerometer）](https://en.wikipedia.org/wiki/Accelerometer)。

- 作为 [LSM303DLHC](https://www.st.com/en/mems-and-sensors/lsm303dlhc.html) 芯片一部分的[磁力计（magnetometer）](https://en.wikipedia.org/wiki/Magnetometer)。

- 作为 [L3GD20](https://www.pololu.com/file/0J563/L3GD20.pdf) 芯片一部分的[陀螺仪（gyroscope）](https://en.wikipedia.org/wiki/Gyroscope)。

- 8 个用户 LED，排列成指南针形状。

- 第二颗微控制器：[STM32F103](https://www.st.com/en/microcontrollers/stm32f103cb.html)。该微控制器实际上是板载编程器/调试器的一部分，并连接到名为 “USB ST-LINK” 的 Mini-USB 端口。

更详细的特性列表与进一步规格说明，请参阅 [STMicroelectronics](https://www.st.com/en/evaluation-tools/stm32f3discovery.html) 网站。

一句提醒：若要对板子施加外部信号，请务必小心。微控制器 STM32F303VCT6 的引脚标称电压为 3.3 伏。更多信息请查阅[手册中的 6.2 Absolute maximum ratings 一节](https://www.st.com/resource/en/datasheet/stm32f303vc.pdf)。
