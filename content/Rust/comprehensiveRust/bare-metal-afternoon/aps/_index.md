+++
title = "1 应用处理器"
date = 2026-08-11T11:30:00+08:00
weight = 312
type = "docs"
description = "应用处理器 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/aps.html](https://google.github.io/comprehensive-rust/bare-metal/aps.html)

# 1 应用处理器

到目前为止，我们已经讨论了微控制器，例如 Arm Cortex-M 系列。
这些通常是资源非常有限的小型系统。

具有更多资源的更大系统通常称为应用程序处理器，
围绕 ARM Cortex-A 或 Intel Atom 等处理器构建。

为简单起见，我们将仅使用 QEMU 的 aarch64
['virt'](https://qemu-project.gitlab.io/qemu/system/arm/virt.html) 板。

> - 一般来说，微控制器没有 MMU 或多层
>   特权（Arm CPU 上的异常级别，x86 上的环）。
> - 应用处理器拥有更多的资源，并且经常运行操作系统，
>   而不是在启动时直接执行目标应用程序。
> - QEMU 支持模拟各种不同的机器或板模型
>   建筑学。 “虚拟”板不对应于任何特定的真实板
>   硬件，但纯粹是为虚拟机设计的。
> - 我们仍然将该板称为裸机，就好像我们正在编写一个
>   操作系统。

