+++
title = "1 欢迎"
date = 2026-08-11T11:30:00+08:00
weight = 294
type = "docs"
description = "01-欢迎 — Comprehensive Rust"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [Comprehensive Rust](https://google.github.io/comprehensive-rust/)

> 原文链接: [https://google.github.io/comprehensive-rust/bare-metal.html](https://google.github.io/comprehensive-rust/bare-metal.html)

# 1 欢迎

这是一门独立的一日课程，主题是裸机（bare-metal）Rust，面向已熟悉 Rust 基础（例如学完 Comprehensive Rust）的学员，理想情况下也具备用 C 等其他语言做裸机编程的经验。

今天我们讨论「裸机」Rust：在没有操作系统的情况下运行 Rust 代码。内容分为几部分：

- 什么是 `no_std` Rust？
- 为微控制器编写固件。
- 为应用处理器编写 bootloader / 内核代码。
- 一些对裸机 Rust 开发有用的 crate。

微控制器部分以 [BBC micro:bit](https://microbit.org/) v2 为例。它是一块基于 Nordic nRF52833 微控制器的[开发板](https://tech.microbit.org/hardware/)，带有 LED、按钮、经 I2C 连接的加速度计与指南针，以及板载 SWD 调试器。

开始前先安装后面会用到的工具。在 gLinux 或 Debian 上：

```bash
sudo apt install gdb-multiarch libudev-dev picocom pkg-config qemu-system-arm build-essential
rustup update
rustup target add aarch64-unknown-none thumbv7em-none-eabihf
rustup component add llvm-tools-preview
cargo install cargo-binutils
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/probe-rs/probe-rs/releases/latest/download/probe-rs-tools-installer.sh | sh
```

并让 `plugdev` 组用户能访问 micro:bit 编程器：

```bash
echo 'SUBSYSTEM=="hidraw", ATTRS{idVendor}=="0d28", MODE="0660", GROUP="logindev", TAG+="uaccess"' |\
  sudo tee /etc/udev/rules.d/50-microbit.rules
sudo udevadm control --reload-rules
```

若设备可用，`lsusb` 输出中应能看到 “NXP ARM mbed”。若在 Chromebook 上的 Linux 环境中，还需通过
`chrome://os-settings/crostini/sharedUsbDevices` 把 USB 设备共享给 Linux。

在 MacOS 上：

```bash
xcode-select --install
brew install gdb picocom qemu
rustup update
rustup target add aarch64-unknown-none thumbv7em-none-eabihf
rustup component add llvm-tools-preview
cargo install cargo-binutils
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/probe-rs/probe-rs/releases/latest/download/probe-rs-tools-installer.sh | sh
```
