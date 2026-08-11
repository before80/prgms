+++
title = "3.7 `probe-rs` 与 `cargo-embed`"
date = 2026-08-11T11:30:00+08:00
weight = 305
type = "docs"
description = "`probe-rs` 与 `cargo-embed` — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal/microcontrollers/probe-rs.html](https://google.github.io/comprehensive-rust/bare-metal/microcontrollers/probe-rs.html)

# 3.7 `probe-rs` 与 `cargo-embed`

[probe-rs](https://probe.rs/) 是一套方便的嵌入式调试工具集，类似 OpenOCD，但集成更好。

- 经 CMSIS-DAP、ST-Link 与 J-Link 探针支持 SWD（Serial Wire Debug）与 JTAG
- GDB stub 与 Microsoft DAP（Debug Adapter Protocol）服务器
- Cargo 集成

`cargo-embed` 是一个 cargo 子命令，用于构建并烧录二进制、记录 RTT（Real Time Transfers）输出并连接 GDB。由项目目录中的 `Embed.toml` 配置。

> - [CMSIS-DAP](https://arm-software.github.io/CMSIS_5/DAP/html/index.html) 是 Arm 制定的 USB 协议标准，供在线调试器访问各类 Arm Cortex 处理器的 CoreSight Debug Access Port。BBC micro:bit 的板载调试器就使用它。
> - ST-Link 是 ST Microelectronics 的一系列在线调试器，J-Link 是 SEGGER 的一系列产品。
> - Debug Access Port 通常是 5 针 JTAG 或 2 针 Serial Wire Debug。
> - probe-rs 是一个库，若有需要也可以集成到自己的工具中。
> - [Microsoft Debug Adapter Protocol](https://microsoft.github.io/debug-adapter-protocol/)
>   让 VSCode 等 IDE 能调试运行在任意受支持微控制器上的代码。
> - cargo-embed 是基于 probe-rs 库构建的二进制。
> - RTT（Real Time Transfers）通过若干环形缓冲区，在调试主机与目标之间传输数据。

