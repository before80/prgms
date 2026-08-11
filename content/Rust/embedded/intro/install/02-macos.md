+++
title = "02-macOS"
date = 2026-08-01T10:38:00+08:00
weight = 26
type = "docs"
description = "macOS（MacOS）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# macOS {#macos}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/intro/install/macos.html](https://doc.rust-lang.org/stable/embedded-book/intro/install/macos.html)


所有工具都可用 [Homebrew] 或 [MacPorts] 安装：

[Homebrew]: http://brew.sh/
[MacPorts]: https://www.macports.org/

## 用 [Homebrew] 安装工具 {#install-tools-with-homebrew}

``` text
$ # GDB
$ brew install arm-none-eabi-gdb

$ # OpenOCD
$ brew install openocd

$ # QEMU
$ brew install qemu
```

> **注意** 若 OpenOCD 崩溃，你可能需要用以下命令安装最新版本：
```text
$ brew install --HEAD openocd
```

## 用 [MacPorts] 安装工具 {#install-tools-with-macports}

``` text
$ # GDB
$ sudo port install arm-none-eabi-gcc

$ # OpenOCD
$ sudo port install openocd

$ # QEMU
$ sudo port install qemu
```



就这些！前往[下一节]。

[下一节]: ../04-verify-installation/
