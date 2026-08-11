+++
title = "04-安装"
date = 2026-08-01T10:38:00+08:00
weight = 24
type = "docs"
description = "安装（Installation）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# 安装 {#installing-the-tools}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/intro/install.html](https://doc.rust-lang.org/stable/embedded-book/intro/install.html)


本页包含部分工具与操作系统无关的安装说明：

### Rust 工具链 {#rust-toolchain}

按 [https://rustup.rs](https://rustup.rs) 的说明安装 rustup。

**注意** 请确保编译器版本等于或高于 `1.31`。`rustc -V` 返回的日期应新于下方所示。

``` text
$ rustc -V
rustc 1.31.1 (b6c32da9b 2018-12-18)
```

出于带宽与磁盘占用考虑，默认安装只支持本地（原生）编译。要为 ARM Cortex-M 架构添加交叉编译支持，请选择下列编译目标之一。对于本书示例所用的 STM32F3DISCOVERY 开发板，请使用 `thumbv7em-none-eabihf` 目标。
[查找最适合你的 Cortex-M。](https://developer.arm.com/ip-products/processors/cortex-m#c-7d3b69ce-5b17-4c9e-8f06-59b605713133)

Cortex-M0、M0+ 与 M1（ARMv6-M 架构）：
``` console
rustup target add thumbv6m-none-eabi
```

Cortex-M3（ARMv7-M 架构）：
``` console
rustup target add thumbv7m-none-eabi
```

Cortex-M4 与 M7（无硬件浮点，ARMv7E-M 架构）：
``` console
rustup target add thumbv7em-none-eabi
```

Cortex-M4F 与 M7F（有硬件浮点，ARMv7E-M 架构）：
``` console
rustup target add thumbv7em-none-eabihf
```

Cortex-M23（ARMv8-M 架构）：
``` console
rustup target add thumbv8m.base-none-eabi
```

Cortex-M33 与 M35P（ARMv8-M 架构）：
``` console
rustup target add thumbv8m.main-none-eabi
```

Cortex-M33F 与 M35PF（有硬件浮点，ARMv8-M 架构）：
``` console
rustup target add thumbv8m.main-none-eabihf
```


### `cargo-binutils` {#cargo-binutils}

``` text
cargo install cargo-binutils

rustup component add llvm-tools
```
WINDOWS：前置条件是已安装 C++ Build Tools for Visual Studio 2019。https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16
### `cargo-generate` {#cargo-generate}

我们稍后会用它从模板生成项目。

``` console
cargo install cargo-generate
```

注意：在某些 Linux 发行版（例如 Ubuntu）上，安装 cargo-generate 之前可能需要先安装 `libssl-dev` 与 `pkg-config` 包。

### 特定于操作系统的说明 {#os-specific-instructions}

现在请按你所使用的操作系统跟随对应说明：

- [Linux](01-linux/)
- [Windows](03-windows/)
- [macOS](02-macos/)

## 本章其它页面 {#other-pages-in-this-chapter}

- [Linux](01-linux/)
- [macOS](02-macos/)
- [Windows](03-windows/)
- [验证安装](04-verify-installation/)
