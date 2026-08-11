+++
title = "05-可移植性"
date = 2026-08-01T10:38:00+08:00
weight = 82
type = "docs"
description = "可移植性（Portability）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 可移植性 {#portability}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/portability/](https://doc.rust-lang.org/stable/embedded-book/portability/)


在嵌入式环境中，可移植性是一个非常重要的话题：每个厂商乃至同一制造商的每个产品系列都提供不同的外设与能力，与外设交互的方式也会随之变化。

抹平这类差异的一种常见方式是通过称为硬件抽象层（Hardware Abstraction Layer）或 **HAL** 的一层。

> 硬件抽象是软件中的一组例程，用来模拟某些平台相关细节，使程序能直接访问硬件资源。
>
> 它们往往通过向硬件提供标准的操作系统（OS）调用，让程序员能够编写与设备无关、高性能的应用程序。
>
> *Wikipedia: [Hardware Abstraction Layer]*

[Hardware Abstraction Layer]: https://en.wikipedia.org/wiki/Hardware_abstraction

嵌入式系统在这方面有些特殊，因为我们通常没有操作系统和用户可安装的软件，而是作为整体编译的固件镜像，还有许多其他约束。因此，虽然 Wikipedia 所定义的传统做法理论上可行，但它多半不是确保可移植性的最高效途径。

在 Rust 中我们怎么做？请看 **[embedded-hal]**……

## 什么是 [embedded-hal]？ {#what-is-embedded-hal}

简而言之，它是一组 trait，定义了 **HAL 实现**、**驱动** 与 **应用（或固件）** 之间的实现契约。这些契约既包括能力（即若某类型实现了某个 trait，则该 **HAL 实现** 提供某种能力），也包括方法（即若你能构造实现某 trait 的类型，就保证可以使用该 trait 中指定的方法）。

典型的分层可能如下所示：

![](../assets/rust_layers.svg)

**[embedded-hal]** 中定义的部分 trait 有：
* GPIO（输入与输出引脚）
* 串行通信
* I2C
* SPI
* 定时器/倒计时
* 模数转换（ADC）

拥有 **embedded-hal** trait 以及实现与使用它们的 crate 的主要原因，是控制复杂度。如果你考虑到一个应用可能既要实现硬件中外设的使用，又要实现应用逻辑，还可能要实现额外硬件组件的驱动，就很容易看出可复用性非常有限。用数学表达：若 **M** 是外设 HAL 实现的数量，**N** 是驱动的数量，若我们为每个应用都重新发明轮子，最终会有 **M\*N** 个实现；而通过使用 **[embedded-hal]** trait 提供的 *API*，实现复杂度会趋向 **M+N**。当然还有其他好处，例如由于定义清晰、即用可用的 API，减少反复试错。

## [embedded-hal] 的使用者 {#users-of-the-embedded-hal}

如上所述，HAL 有三类主要使用者：

### HAL 实现 {#hal-implementation}

HAL 实现提供硬件与 HAL trait 使用者之间的接口。典型实现由三部分组成：
* 一个或多个硬件相关类型
* 创建并初始化此类类型的函数，通常提供各种配置选项（速度、工作模式、所用引脚等）
* 对该类型的一个或多个 **[embedded-hal]** trait 的 `impl`

这样的 **HAL 实现** 可以有多种风格：
* 通过底层硬件访问，例如经由寄存器
* 通过操作系统，例如在 Linux 下使用 `sysfs`
* 通过适配器，例如用于单元测试的类型 mock
* 通过硬件适配器驱动，例如 I2C 多路复用器或 GPIO 扩展器

### 驱动 {#driver}

驱动为一组内部或外部组件实现自定义功能，这些组件连接到实现了 [embedded-hal] trait 的外设。此类驱动的典型例子包括各种传感器（温度、磁力计、加速度计、光线）、显示设备（LED 阵列、LCD 显示）和执行器（电机、发射器）。

驱动必须用实现了 [embedded-hal] 某一 `trait` 的类型实例来初始化（通过 trait bound 保证），并提供带有自定义方法集的自身类型实例，以便与被驱动设备交互。

### 应用 {#application}

应用把各个部分粘合在一起，并确保实现期望的功能。在不同系统间移植时，这部分通常需要最多的适配工作，因为应用需要通过 HAL 实现正确初始化真实硬件，而不同硬件的初始化方式不同，有时差异很大。用户选择往往也扮演重要角色，因为组件可以物理连接到不同端子，硬件总线有时需要外部硬件来匹配配置，或者在使用内部外设时存在不同权衡（例如有多个能力不同的定时器可用，或外设之间存在冲突）。

[embedded-hal]: https://crates.io/crates/embedded-hal
