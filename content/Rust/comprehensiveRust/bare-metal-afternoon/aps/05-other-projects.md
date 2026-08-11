+++
title = "1.10 其他项目"
date = 2026-08-11T11:30:00+08:00
weight = 331
type = "docs"
description = "05-其他项目 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/aps/other-projects.html](https://google.github.io/comprehensive-rust/bare-metal/aps/other-projects.html)

# 1.10 其他项目

- [oreboot](https://github.com/oreboot/oreboot)
  - “没有 C 的 coreboot”。
  - 支持 x86、aarch64 和 RISC-V。
  - 依赖于 LinuxBoot 而不是本身拥有许多驱动程序。
- [Rust RaspberryPi 操作系统教程](https://github.com/rust-embedded/rust-raspberrypi-OS-tutorials)
  - 初始化、UART 驱动程序、简单引导加载程序、JTAG、异常级别、
    异常处理，页表。
  - Rust 中关于缓存维护和初始化的一些警告，而不是
    必然是复制生产代码的好例子。
- [`cargo-call-stack`](https://crates.io/crates/cargo-call-stack)
  - 静态分析以确定最大堆栈使用率。

> - RaspberryPi OS 教程在 MMU 和缓存之前运行 Rust 代码
>   已启用。这将读取和写入内存（例如堆栈）。然而，这已经
>   本届会议开始时提到的关于不结盟的问题
>   访问和缓存一致性。

