+++
title = "01-Linux"
date = 2026-08-01T10:38:00+08:00
weight = 25
type = "docs"
description = "Linux"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Embedded Rust Book](https://doc.rust-lang.org/stable/embedded-book/)

# Linux {#linux}


> 原文链接: [https://doc.rust-lang.org/stable/embedded-book/intro/install/linux.html](https://doc.rust-lang.org/stable/embedded-book/intro/install/linux.html)


以下是若干 Linux 发行版的安装命令。

## 软件包 {#packages}

- Ubuntu 18.04 或更新 / Debian stretch 或更新

> **注意** `gdb-multiarch` 是你用来调试 ARM Cortex-M 程序的 GDB 命令

<!-- Debian stretch -->
<!-- GDB 7.12 -->
<!-- OpenOCD 0.9.0 -->
<!-- QEMU 2.8.1 -->

<!-- Ubuntu 18.04 -->
<!-- GDB 8.1 -->
<!-- OpenOCD 0.10.0 -->
<!-- QEMU 2.11.1 -->

``` console
sudo apt install gdb-multiarch openocd qemu-system-arm
```

- Ubuntu 14.04 与 16.04

> **注意** `arm-none-eabi-gdb` 是你用来调试 ARM Cortex-M 程序的 GDB 命令

<!-- Ubuntu 14.04 -->
<!-- GDB 7.6 (!) -->
<!-- OpenOCD 0.7.0 (?) -->
<!-- QEMU 2.0.0 (?) -->

``` console
sudo apt install gdb-arm-none-eabi openocd qemu-system-arm
```

- Fedora 27 或更新

<!-- Fedora 27 -->
<!-- GDB 7.6 (!) -->
<!-- OpenOCD 0.10.0 -->
<!-- QEMU 2.10.2 -->

``` console
sudo dnf install gdb openocd qemu-system-arm
```

- Arch Linux

> **注意** `arm-none-eabi-gdb` 是你用来调试 ARM Cortex-M 程序的 GDB 命令

``` console
sudo pacman -S arm-none-eabi-gdb qemu-system-arm openocd
```

## udev 规则 {#udev-rules}

这条规则让你可以在没有 root 权限的情况下，用 OpenOCD 操作 Discovery 开发板。

创建文件 `/etc/udev/rules.d/70-st-link.rules`，内容如下。

``` text
# STM32F3DISCOVERY rev A/B - ST-LINK/V2
ATTRS{idVendor}=="0483", ATTRS{idProduct}=="3748", TAG+="uaccess"

# STM32F3DISCOVERY rev C+ - ST-LINK/V2-1
ATTRS{idVendor}=="0483", ATTRS{idProduct}=="374b", TAG+="uaccess"
```

然后用以下命令重新加载全部 udev 规则：

``` console
sudo udevadm control --reload-rules
```

若板子已插入笔记本，请拔出后再插上。

可通过运行此命令检查权限：

``` console
lsusb
```

应显示类似如下内容：

```text
(..)
Bus 001 Device 018: ID 0483:374b STMicroelectronics ST-LINK/V2.1
(..)
```

记下总线与设备编号。用这些编号构造类似 `/dev/bus/usb/<bus>/<device>` 的路径。然后像这样使用该路径：

``` console
ls -l /dev/bus/usb/001/018
```

```text
crw-------+ 1 root root 189, 17 Sep 13 12:34 /dev/bus/usb/001/018
```

```console
getfacl /dev/bus/usb/001/018 | grep user
```

```text
user::rw-
user:you:rw-
```

权限后追加的 `+` 表示存在扩展权限。`getfacl` 命令表明用户 `you` 可以使用该设备。

现在，前往[下一节]。

[下一节]: ../04-verify-installation/
