+++
title = "03-工具链"
date = 2026-08-01T10:38:00+08:00
weight = 14
type = "docs"
description = "工具链（Tooling）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 工具链 {#tooling}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/intro/tooling.html](https://doc.rust-lang.org/stable/embedded-book/intro/tooling.html)


处理微控制器会用到多种不同工具，因为我们将面对与笔记本不同的架构，并且必须在*远程*设备上运行与调试程序。

我们将使用下列所有工具。未指定最低版本时，任何较新版本通常都可用；我们也列出了已测试的版本。

- Rust 1.31、1.31-beta，或更新的工具链，外加 ARM Cortex-M 编译支持。
- [`cargo-binutils`](https://github.com/rust-embedded/cargo-binutils) ~0.1.4
- [`qemu-system-arm`](https://www.qemu.org/)。已测试版本：3.0.0
- OpenOCD >=0.8。已测试版本：v0.9.0 与 v0.10.0
- 带 ARM 支持的 GDB。强烈建议 7.12 或更新版本。已测试版本：7.10、7.11、7.12 与 8.1
- [`cargo-generate`](https://github.com/ashleygwilliams/cargo-generate) 或 `git`。
  这些工具是可选的，但会让跟随本书更容易。

下文解释我们为何使用这些工具。安装说明见下一页。

## `cargo-generate` 或 `git` {#cargo-generate-or-git}

裸机程序是非标准（`no_std`）的 Rust 程序，需要调整链接过程才能得到正确的内存布局。
这需要一些额外文件（如链接脚本）与设置（如链接器标志）。我们已把这些打包装进模板，
你只需填入缺失信息（如项目名称与目标硬件特性）。

我们的模板兼容 `cargo-generate`：一个从模板创建新 Cargo 项目的 Cargo 子命令。你也可以用 `git`、`curl`、`wget` 或浏览器下载模板。

## `cargo-binutils` {#cargo-binutils}

`cargo-binutils` 是一组 Cargo 子命令，便于使用随 Rust 工具链附带的 LLVM 工具。这些工具包括 LLVM 版本的 `objdump`、`nm` 与 `size`，用于检查二进制文件。

相对 GNU binutils，使用这些工具的优势是：(a) 安装 LLVM 工具在各操作系统上是同一条命令（`rustup component add llvm-tools`）；(b) 像 `objdump` 这样的工具支持 `rustc` 支持的全部架构——从 ARM 到 x86_64——因为它们共享同一 LLVM 后端。

## `qemu-system-arm` {#qemu-system-arm}

QEMU 是模拟器。这里我们使用能完整模拟 ARM 系统的变体。我们用 QEMU 在宿主机上运行嵌入式程序。因此即使手头没有硬件，你也可以跟随本书的部分内容！

# 嵌入式 Rust 调试工具链 {#tooling-for-embedded-rust-debugging}

## 概览 {#overview}

在 Rust 中调试嵌入式系统需要专门工具，包括管理调试过程的软件、用于检查与控制程序执行的调试器，以及促进主机与嵌入式设备交互的硬件探针。本文概述 Probe-rs 与 OpenOCD 等关键软件工具（它们简化并支撑调试过程），以及 GDB 与 Probe-rs Visual Studio Code 扩展等主要调试器。此外也会介绍 Rusty-probe、ST-Link、J-Link 与 MCU-Link 等关键硬件探针，它们对有效调试与编程嵌入式设备不可或缺。

## 驱动调试工具的软件 {#software-that-drives-debugging-tools}

### Probe-rs {#probe-rs}

Probe-rs 是面向 Rust、用于嵌入式系统调试器的现代软件。与 OpenOCD 不同，Probe-rs 以简洁为目标，旨在减轻其它调试方案中常见的配置负担。它支持多种探针与目标，提供与嵌入式硬件交互的高层接口。Probe-rs 直接与 Rust 工具链集成，并通过扩展与 Visual Studio Code 集成，使开发者能够简化调试工作流。

### OpenOCD（Open On-Chip Debugger） {#openocd-open-on-chip-debugger}

OpenOCD 是用于调试、测试与编程嵌入式系统的开源软件工具。它在主机系统与嵌入式硬件之间提供接口，支持 JTAG 与 SWD（Serial Wire Debug）等多种传输层。OpenOCD 与调试器 GDB 集成。OpenOCD 支持广泛，文档详尽且社区庞大，但配置可能复杂，尤其是在定制嵌入式环境中。

## 调试器 {#debuggers}

调试器让开发者能够检查并控制程序执行，以便识别与修正错误或 bug。它提供设置断点、逐行单步执行代码、检查变量值与内存状态等功能。调试器对彻底的软件开发与维护至关重要，使开发者能够确保代码在各种条件下按预期行为运行。

调试器能够：
 * 与内存映射寄存器交互。
 * 设置断点/观察点（Breakpoints/Watchpoints）。
 * 读写内存映射寄存器。
 * 检测 MCU 因调试事件而停机。
 * 在遇到调试事件后继续 MCU 执行。
 * 擦除并写入微控制器的 FLASH。

### Probe-rs Visual Studio Code 扩展 {#probe-rs-visual-studio-code-extension}

Probe-rs 有 Visual Studio Code 扩展，可在无需大量设置的情况下提供流畅的调试体验。通过该连接，开发者可以使用 pretty printing 与详细错误信息等 Rust 特有功能，使调试过程与 Rust 生态保持一致。

### TRACE32 {#trace32}

TRACE32 是 Lauterbach 为嵌入式系统开发的专业调试与跟踪方案。它支持包括 ARM 与 RISC-V 在内的多种处理器架构，并通过 JTAG、SWD 以及各种跟踪接口连接到目标硬件。TRACE32 提供多核调试、复杂断点与实时跟踪分析等高级调试能力。它使用标准 ELF/DWARF 调试信息，因此与用常规工具链构建的 Rust 二进制兼容。

### GDB（GNU Debugger） {#gdb-gnu-debugger}

GDB 是多功能调试工具，可让开发者在程序运行时或崩溃后检查其状态。对于嵌入式 Rust，GDB 通过 OpenOCD 或其它调试服务器连接到目标系统，以与嵌入式代码交互。GDB 高度可配置，支持远程调试、变量检查与条件断点等功能。它可用于多种平台，并对 pretty printing 与 IDE 集成等 Rust 特定调试需求有广泛支持。

## 探针（Probes） {#probes}

硬件探针是嵌入式系统开发与调试中用于促进主机与目标嵌入式设备通信的设备。它通常支持 JTAG 或 SWD 等协议，从而能够对嵌入式系统上的微控制器或微处理器进行编程、调试与分析。硬件探针对开发者设置断点、单步执行代码、检查内存与处理器寄存器至关重要，使他们能实时诊断并修复问题。

### Rusty-probe {#rusty-probe}

Rusty-probe 是开源的基于 USB 的硬件调试探针，设计用于与 probe-rs 配合。Rusty-Probe 与 probe-rs 的组合为从事嵌入式 Rust 应用的开发者提供了易用且经济的方案。

### ST-Link {#st-link}

ST-Link 是 STMicroelectronics 主要为 STM32 与 STM8 微控制器系列开发的流行调试与编程探针。它通过 JTAG 或 SWD（Serial Wire Debug）接口支持调试与编程。ST-Link 因其对 STMicroelectronics 广泛开发板的直接支持，以及与主流 IDE 的集成而被广泛使用，成为使用 STM 微控制器的开发者的便捷选择。

### J-Link {#j-link}

J-Link 由 SEGGER Microcontroller 开发，是稳健且多功能的调试器，支持远不止 ARM 的多种 CPU 内核与设备，例如 RISC-V。以高性能与可靠性著称，J-Link 支持包括 JTAG、SWD 与 fine-pitch JTAG 在内的多种通信接口。它因 Flash 中无限断点等高级功能，以及与众多开发环境的兼容性而受到青睐。

### MCU-Link {#mcu-link}

MCU-Link 是 NXP Semiconductors 提供的调试探针，也可作为编程器使用。它支持多种 ARM Cortex 微控制器，并能与 MCUXpresso IDE 等开发工具无缝协作。MCU-Link 以其多功能性与可负担性尤为突出，对爱好者、教育者与专业开发者都是易于获取的选项。
