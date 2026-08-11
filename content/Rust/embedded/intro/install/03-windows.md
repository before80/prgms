+++
title = "03-Windows"
date = 2026-08-01T10:38:00+08:00
weight = 27
type = "docs"
description = "Windows"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# Windows {#windows}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/intro/install/windows.html](https://doc.rust-lang.org/stable/embedded-book/intro/install/windows.html)


## `arm-none-eabi-gdb` {#arm-none-eabi-gdb}

ARM 为 Windows 提供 `.exe` 安装程序。从[这里][gcc]获取并按说明操作。
在安装过程即将结束前，勾选/选择 “Add path to environment variable” 选项。然后验证工具已在你的 `%PATH%` 中：

``` text
$ arm-none-eabi-gdb -v
GNU gdb (GNU Tools for Arm Embedded Processors 7-2018-q2-update) 8.1.0.20180315-git
(..)
```

[gcc]: https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads

## OpenOCD {#openocd}

OpenOCD 没有面向 Windows 的官方二进制发行版，但若你不想自行编译，xPack 项目提供了二进制发行版，见[这里][openocd]。按所提供的安装说明操作。然后更新你的 `%PATH%` 环境变量，把二进制安装路径加入其中。（若你使用了简易安装，路径类似 `C:\Users\USERNAME\AppData\Roaming\xPacks\@xpack-dev-tools\openocd\0.10.0-13.1\.content\bin\`）

[openocd]: https://xpack.github.io/openocd/

用以下命令验证 OpenOCD 已在你的 `%PATH%` 中：

``` text
$ openocd -v
Open On-Chip Debugger 0.10.0
(..)
```

## QEMU {#qemu}

从[官方网站][qemu]获取 QEMU。

[qemu]: https://www.qemu.org/download/#windows

## ST-LINK USB 驱动 {#st-link-usb-driver}

你还需要安装[此 USB 驱动]，否则 OpenOCD 无法工作。按安装程序说明操作，并确保安装正确版本（32 位或 64 位）的驱动。

[此 USB 驱动]: http://www.st.com/en/embedded-software/stsw-link009.html

就这些！前往[下一节]。

[下一节]: ../04-verify-installation/
