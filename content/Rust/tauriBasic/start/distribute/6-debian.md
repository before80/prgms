+++
title = "6 Debian"
date = 2026-09-25T21:31:08+08:00
weight = 6
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/distribute/debian/](https://tauri.app/distribute/debian/)

Tauri 打包器生成的默认 Debian 包已经包含把应用发布到基于 Debian 的 Linux 发行版所需的一切：定义应用的图标、生成 Desktop 文件，并指定依赖 `libwebkit2gtk-4.1-0` 和 `libgtk-3-0`，以及当你的应用使用系统托盘时的 `libappindicator3-1`。

{{% alert title="注意" %}}

macOS 和 Linux 上的 GUI 应用不会从你的 shell dotfile（`.bashrc`、`.bash_profile`、`.zshrc` 等）继承 `$PATH`。请查看 Tauri 的 [fix-path-env-rs](https://github.com/tauri-apps/fix-path-env-rs) crate 来修复这个问题。

{{% /alert %}}

## 限制

glibc 之类的核心库经常会破坏与旧系统的兼容性。因此，你必须使用你打算支持的最旧基础系统来构建 Tauri 应用，并且该系统还要提供 Tauri v2 所需的 WebKitGTK 4.1 软件包。Ubuntu 22.04 和 Debian 12 是合适的基线示例，因为它们从标准软件仓库提供 `libwebkit2gtk-4.1-dev`。在更新的基础系统上构建可能提高应用所需的最低 glibc 版本，因此在旧系统上运行时可能遇到 `/usr/lib/libc.so.6: version 'GLIBC_2.33' not found` 这样的运行时错误。我们建议使用 Docker 容器或 GitHub Actions 为 Linux 构建你的 Tauri 应用。

更多信息请参阅 [tauri-apps/tauri#1355](https://github.com/tauri-apps/tauri/issues/1355) 和 [rust-lang/rust#57497](https://github.com/rust-lang/rust/issues/57497)，以及 [AppImage 指南](https://docs.appimage.org/reference/best-practices.html#binaries-compiled-on-old-enough-base-system)。

## 自定义文件

若你需要更多控制，Tauri 为 Debian 包暴露了一些配置。

如果你的应用依赖额外的系统依赖，可以在 `tauri.conf.json > bundle > linux > deb` 中指定它们。

要把自定义文件加入 Debian 包，你可以在 `tauri.conf.json > bundle > linux > deb > files` 中提供文件或文件夹列表。该配置对象把 Debian 包中的路径映射到文件系统上的文件路径（相对于 `tauri.conf.json` 文件）。下面是一个配置示例：

```json
{
  "bundle": {
    "linux": {
      "deb": {
        "files": {
          "/usr/share/README.md": "../README.md", // 把 README.md 复制到 /usr/share/README.md
          "/usr/share/assets": "../assets/" // 把整个 assets 目录复制到 /usr/share/assets
        }
      }
    }
  }
}
```

## 为 ARM 设备交叉编译

本指南涵盖手动编译。关于利用 QEMU 构建应用的示例 workflow，请参阅我们的 [GitHub Action 指南](../pipelines/2-github/#arm-runner-编译)。那样会慢得多，但也能构建 AppImage。

当你不需要频繁编译应用，并且偏好一次性配置时，手动编译是合适的。以下步骤假设你使用基于 Debian/Ubuntu 的 Linux 发行版。

### 1. 为你想要的架构安装 Rust 目标

- ARMv7（32 位）：`rustup target add armv7-unknown-linux-gnueabihf`
- ARMv8（ARM64，64 位）：`rustup target add aarch64-unknown-linux-gnu`

### 2. 安装所选架构对应的链接器

- ARMv7：`sudo apt install gcc-arm-linux-gnueabihf`
- ARMv8（ARM64）：`sudo apt install gcc-aarch64-linux-gnu`

### 3. 打开或创建文件 `<project-root>/.cargo/config.toml`，并相应加入以下配置

```toml
[target.armv7-unknown-linux-gnueabihf]
linker = "arm-linux-gnueabihf-gcc"

[target.aarch64-unknown-linux-gnu]
linker = "aarch64-linux-gnu-gcc"
```

### 4. 在包管理器中启用相应架构

- ARMv7：`sudo dpkg --add-architecture armhf`
- ARMv8（ARM64）：`sudo dpkg --add-architecture arm64`

### 5. 调整软件包源

在 Debian 上这一步应该不需要，但在其它发行版上，你可能需要编辑 /etc/apt/sources.list 以包含 ARM 架构变体。例如在 Ubuntu 22.04 上，把以下行加到文件末尾（记得把 jammy 换成你的 Ubuntu 版本代号）：

```
deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy main restricted
deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy-updates main restricted
deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy universe
deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy-updates universe
deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy multiverse
deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy-updates multiverse
deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy-backports main restricted universe multiverse
deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy-security main restricted
deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy-security universe
deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy-security multiverse
```

然后，为避免主软件包出现问题，你必须给文件中原有的其它所有行加上正确的主架构。对标准 64 位系统，你需要加上 [arch=amd64]，Ubuntu 22.04 上完整的文件大致如下：

<details>
<summary>查看答案</summary>

```
# See http://help.ubuntu.com/community/UpgradeNotes for how to upgrade to
# newer versions of the distribution.
deb [arch=amd64] http://archive.ubuntu.com/ubuntu/ jammy main restricted
# deb-src http://archive.ubuntu.com/ubuntu/ jammy main restricted

## Major bug fix updates produced after the final release of the
## distribution.
deb [arch=amd64] http://archive.ubuntu.com/ubuntu/ jammy-updates main restricted
# deb-src http://archive.ubuntu.com/ubuntu/ jammy-updates main restricted

## N.B. software from this repository is ENTIRELY UNSUPPORTED by the Ubuntu
## team. Also, please note that software in universe WILL NOT receive any
## review or updates from the Ubuntu security team.
deb [arch=amd64] http://archive.ubuntu.com/ubuntu/ jammy universe
# deb-src http://archive.ubuntu.com/ubuntu/ jammy universe
deb [arch=amd64] http://archive.ubuntu.com/ubuntu/ jammy-updates universe
# deb-src http://archive.ubuntu.com/ubuntu/ jammy-updates universe

## N.B. software from this repository is ENTIRELY UNSUPPORTED by the Ubuntu
## team, and may not be under a free licence. Please satisfy yourself as to
## your rights to use the software. Also, please note that software in
## multiverse WILL NOT receive any review or updates from the Ubuntu
## security team.
deb [arch=amd64] http://archive.ubuntu.com/ubuntu/ jammy multiverse
# deb-src http://archive.ubuntu.com/ubuntu/ jammy multiverse
deb [arch=amd64] http://archive.ubuntu.com/ubuntu/ jammy-updates multiverse

## N.B. software from this repository may not have been tested as
## extensively as that contained in the main release, although it includes
## newer versions of some applications which may provide useful features.
## Also, please note that software in backports WILL NOT receive any review
## or updates from the Ubuntu security team.
deb [arch=amd64] http://archive.ubuntu.com/ubuntu/ jammy-backports main restricted universe multiverse
# deb-src http://archive.ubuntu.com/ubuntu/ jammy-backports main restricted universe multiverse

deb [arch=amd64] http://security.ubuntu.com/ubuntu/ jammy-security main restricted
# deb-src http://security.ubuntu.com/ubuntu/ jammy-security main restricted
deb [arch=amd64] http://security.ubuntu.com/ubuntu/ jammy-security universe
# deb-src http://security.ubuntu.com/ubuntu/ jammy-security universe
deb [arch=amd64] http://security.ubuntu.com/ubuntu/ jammy-security multiverse
# deb-src http://security.ubuntu.com/ubuntu/ jammy-security multiverse

deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy main restricted
deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy-updates main restricted
deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy universe
deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy-updates universe
deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy multiverse
deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy-updates multiverse
deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy-backports main restricted universe multiverse
deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy-security main restricted
deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy-security universe
deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports jammy-security multiverse
```

</details>

### 6. 更新软件包信息

`sudo apt-get update && sudo apt-get upgrade -y`

### 7. 安装所选架构所需的 webkitgtk 库

- ARMv7：`sudo apt install libwebkit2gtk-4.1-dev:armhf`
- ARMv8（ARM64）：`sudo apt install libwebkit2gtk-4.1-dev:arm64`

### 8. 安装 OpenSSL 或使用 vendored 版本

这不总是必需，因此你可能想先继续，看看是否出现 `Failed to find OpenSSL development headers` 之类的错误。

- 要么在系统范围内安装开发头文件：
  - ARMv7：`sudo apt install libssl-dev:armhf`
  - ARMv8（ARM64）：`sudo apt install libssl-dev:arm64`
- 要么为 OpenSSL Rust crate 启用 vendor 特性，这会影响所有使用相同次要版本的其它 Rust 依赖。你可以在 `Cargo.toml` 文件的 dependencies 部分加入以下内容：

```toml
openssl-sys = {version = "0.9", features = ["vendored"]}
```

### 9. 根据所选架构把 `PKG_CONFIG_SYSROOT_DIR` 设置为相应目录

- ARMv7：`export PKG_CONFIG_SYSROOT_DIR=/usr/arm-linux-gnueabihf/`
- ARMv8（ARM64）：`export PKG_CONFIG_SYSROOT_DIR=/usr/aarch64-linux-gnu/`

### 10. 为你想要的 ARM 版本构建应用

- ARMv7：`cargo tauri build --target armv7-unknown-linux-gnueabihf`
- ARMv8（ARM64）：`cargo tauri build --target aarch64-unknown-linux-gnu`

请根据你是想为 ARMv7 还是 ARMv8（ARM64）交叉编译 Tauri 应用，选择相应的指令集。请注意具体步骤可能因你的 Linux 发行版和配置而异。
