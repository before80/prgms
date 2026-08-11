+++
title = "3.8 其他项目"
date = 2026-08-11T11:30:00+08:00
weight = 307
type = "docs"
description = "07-其他项目 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/microcontrollers/other-projects.html](https://google.github.io/comprehensive-rust/bare-metal/microcontrollers/other-projects.html)

# 3.8 其他项目

- [RTIC](https://rtic.rs/)
  - 「Real-Time Interrupt-driven Concurrency」（实时中断驱动并发）。
  - 共享资源管理、消息传递、任务调度、定时器队列。
- [Embassy](https://embassy.dev/)
  - 带优先级的 `async` executor、定时器、网络、USB。
- [TockOS](https://www.tockos.org/documentation/getting-started)
  - 以安全为重点的 RTOS，支持抢占调度与内存保护单元（MPU）。
- [Hubris](https://hubris.oxide.computer/)
  - Oxide Computer Company 的微内核 RTOS，具备内存保护、非特权驱动、IPC。
- [FreeRTOS 绑定](https://github.com/lobaro/FreeRTOS-rust)。

有些平台提供了 `std` 实现，例如
[esp-idf](https://esp-rs.github.io/book/overview/using-the-standard-library.html)。

> - RTIC 既可以看作 RTOS，也可以看作并发框架。
>   - 它不包含任何 HAL。
>   - 它用 Cortex-M 的 NVIC（Nested Virtual Interrupt Controller）做调度，而不是完整内核。
>   - 仅支持 Cortex-M。
> - Google 在 Titan 安全密钥的 Haven 微控制器上使用 TockOS。
> - FreeRTOS 主要用 C 编写，但有 Rust 绑定可供写应用。

