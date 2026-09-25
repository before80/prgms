+++
title = "13 RPM"
date = 2026-09-25T21:31:08+08:00
weight = 13
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/distribute/rpm/](https://tauri.app/distribute/rpm/)

{{% alert title="注意" %}}
本指南中有些部分是可选的，包括配置脚本以及某些其它步骤。请根据你的具体需求自由调整这些说明。
{{% /alert %}}

本指南涵盖如何分发和管理 RPM 软件包，包括获取包信息、配置脚本、设置依赖以及为包签名。

{{% alert title="注意" %}}

macOS 和 Linux 上的 GUI 应用不会从你的 shell dotfile（`.bashrc`、`.bash_profile`、`.zshrc` 等）继承 `$PATH`。请查看 Tauri 的 [fix-path-env-rs](https://github.com/tauri-apps/fix-path-env-rs) crate 来修复这个问题。

{{% /alert %}}

## 限制

glibc 之类的核心库经常会破坏与旧系统的兼容性。因此，你必须使用你打算支持的最旧基础系统来构建 Tauri 应用，并且该系统还要提供 Tauri v2 所需的 WebKitGTK 4.1 软件包。Ubuntu 22.04 和 Debian 12 是合适的基线示例，因为它们从标准软件仓库提供 `libwebkit2gtk-4.1-dev`。在更新的基础系统上构建可能提高应用所需的最低 glibc 版本，因此在旧系统上运行时可能遇到 `/usr/lib/libc.so.6: version 'GLIBC_2.33' not found` 这样的运行时错误。我们建议使用 Docker 容器或 GitHub Actions 为 Linux 构建你的 Tauri 应用。

更多信息请参阅 [tauri-apps/tauri#1355](https://github.com/tauri-apps/tauri/issues/1355) 和 [rust-lang/rust#57497](https://github.com/rust-lang/rust/issues/57497)，以及 [AppImage 指南](https://docs.appimage.org/reference/best-practices.html#binaries-compiled-on-old-enough-base-system)。

## 配置 RPM 包

Tauri 允许你通过添加脚本、设置依赖、添加许可证、包含自定义文件等方式配置 RPM 包。
关于可配置选项的详细信息，请参阅：[RpmConfig](https://tauri.app/reference/config/#rpmconfig)。

### 为包添加 post、pre 安装／卸载脚本

RPM 包管理器允许你在包的安装或卸载之前或之后运行脚本。例如，你可以用这些脚本在包安装后启动一个服务。

下面是一个添加这些脚本的示例：

1. 在项目的 `src-tauri` 目录中创建一个名为 `scripts` 的文件夹。

```bash
mkdir src-tauri/scripts
```

2. 在该文件夹中创建脚本文件。

```bash
touch src-tauri/scripts/postinstall.sh \
touch src-tauri/scripts/preinstall.sh \
touch src-tauri/scripts/preremove.sh \
touch src-tauri/scripts/postremove.sh
```

现在如果我们查看 `/src-tauri/scripts`，会看到：

```bash
ls src-tauri/scripts/
postinstall.sh  postremove.sh  preinstall.sh  preremove.sh
```

3. 给脚本添加一些内容

```bash
echo "-------------"
echo "This is pre"
echo "Install Value: $1"
echo "Upgrade Value: $1"
echo "Uninstall Value: $1"
echo "-------------"
```

```bash
echo "-------------"
echo "This is post"
echo "Install Value: $1"
echo "Upgrade Value: $1"
echo "Uninstall Value: $1"
echo "-------------"
```

```bash
echo "-------------"
echo "This is preun"
echo "Install Value: $1"
echo "Upgrade Value: $1"
echo "Uninstall Value: $1"
echo "-------------"
```

```bash
echo "-------------"
echo "This is postun"
echo "Install Value: $1"
echo "Upgrade Value: $1"
echo "Uninstall Value: $1"
echo "-------------"
```

4. 把这些脚本加入 `tauri.conf.json` 文件

```json
{
  "bundle": {
    "linux": {
      "rpm": {
        "epoch": 0,
        "files": {},
        "release": "1",
        // 在这里添加脚本
        "preInstallScript": "/path/to/your/project/src-tauri/scripts/prescript.sh",
        "postInstallScript": "/path/to/your/project/src-tauri/scripts/postscript.sh",
        "preRemoveScript": "/path/to/your/project/src-tauri/scripts/prescript.sh",
        "postRemoveScript": "/path/to/your/project/src-tauri/scripts/postscript.sh"
      }
    }
  }
}
```

### 设置 Conflict、Provides、Depends、Files、Obsoletes、DesktopTemplate 与 Epoch

- **conflict**：当包与另一个包冲突时阻止安装。
  例如，你更新了一个你的应用所依赖的 RPM 包，而新版本与你的应用不兼容。

- **provides**：列出你的应用所提供的 RPM 依赖。

- **depends**：列出你的应用运行所需的 RPM 依赖。

- **files**：指定要包含在包中的文件。

- **obsoletes**：列出你的应用所取代（obsolete）的 RPM 依赖。

{{% alert title="注意" %}}
如果该包被安装，被列为 “obsoletes” 的包若存在会被自动移除。
{{% /alert %}}

- **desktopTemplate**：为包添加自定义 desktop 文件。

- **epoch**：基于版本号定义带权重的依赖关系。

{{% alert title="警告" color="warning" %}}
除非必要，不建议使用 epoch，因为它会改变包管理器比较包版本的方式。
关于 epoch 的更多信息，请查看：[RPM 打包指南](https://rpm-packaging-guide.github.io/#epoch-scriptlets-and-triggers)。
{{% /alert %}}

要使用这些选项，请把以下内容加入你的 `tauri.conf.json`：

```json
{
  "bundle": {
    "linux": {
      "rpm": {
        "postRemoveScript": "/path/to/your/project/src-tauri/scripts/postscript.sh",
        "conflicts": ["oldLib.rpm"],
        "depends": ["newLib.rpm"],
        "obsoletes": ["veryoldLib.rpm"],
        "provides": ["coolLib.rpm"],
        "desktopTemplate": "/path/to/your/project/src-tauri/desktop-template.desktop"
      }
    }
  }
}
```

### 为包添加许可证

要为包添加许可证，请在 `src-tauri/cargo.toml` 或 `src-tauri/tauri.conf.json` 文件中加入以下内容：

```toml
[package]
name = "tauri-app"
version = "0.0.0"
description = "A Tauri App"
authors = ["you"]
edition = "2021"
license = "MIT" # 在这里添加许可证
# ...  文件其余部分
```

对于 `src-tauri/tauri.conf.json`：

```json
{
  "bundle": {
    "licenseFile": "../LICENSE", // 把许可证文件的路径放在这里
    "license": "MIT" // 在这里添加许可证
  }
}
```

## 构建 RPM 包

要构建 RPM 包，你可以使用以下命令：

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri build
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri build
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri build
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri build
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri build
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri build
```

{{% /tab %}}

{{< /tabpane >}}

该命令会在 `src-tauri/target/release/bundle/rpm` 目录中构建 RPM 包。

## 为 RPM 包签名

Tauri 允许你在构建过程中用系统里的密钥为包签名。
为此，你需要生成一个 GPG 密钥。

#### 生成 GPG 密钥

要生成 GPG 密钥，你可以使用以下命令：

```bash
gpg --gen-key
```

按照提示生成密钥。

密钥生成后，你需要把它加入环境变量。
你可以在 .bashrc 或 .zshrc 文件中加入以下内容，或者直接在终端中 export：

```bash
export TAURI_SIGNING_RPM_KEY=$(cat /home/johndoe/my_super_private.key)
```

如果密钥有密码短语，你可以把它加入环境变量：

```bash
export TAURI_SIGNING_RPM_KEY_PASSPHRASE=password
```

现在你可以用以下命令构建包：

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri build
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri build
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri build
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri build
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri build
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri build
```

{{% /tab %}}

{{< /tabpane >}}

### 验证签名

{{% alert title="注意" %}}
这只应在本地测试签名时进行。
{{% /alert %}}

在验证签名之前，你需要创建公钥并导入到 RPM 数据库：

```bash
gpg --export -a 'Tauri-App' > RPM-GPG-KEY-Tauri-App
```

```bash
sudo rpm --import RPM-GPG-KEY-Tauri-App
```

导入密钥后，我们必须编辑 `~/.rpmmacros` 文件以使用该密钥。

```bash
%_signature gpg
%_gpg_path /home/johndoe/.gnupg
%_gpg_name Tauri-App
%_gpgbin /usr/bin/gpg2
%__gpg_sign_cmd %{__gpg} \
    gpg --force-v3-sigs --digest-algo=sha1 --batch --no-verbose --no-armor \
    --passphrase-fd 3 --no-secmem-warning -u "%{_gpg_name}" \
    -sbo %{__signature_filename} %{__plaintext_filename}
```

最后，你可以用以下命令验证该包：

```bash
rpm  -v --checksig tauri-app-0.0.0-1.x86_64.rpm
```

## 调试 RPM 包

本节中我们将了解如何通过检查包内容和获取包信息来调试 RPM 包。

### 获取包的信息

要获取包的信息，例如版本、发行号和架构，请使用以下命令：

```bash
rpm -qip package_name.rpm
```

### 查询包的特定信息

例如，如果你想获取包的名称、版本、发行号、架构和大小，请使用以下命令：

```bash
rpm  -qp --queryformat '[%{NAME} %{VERSION} %{RELEASE} %{ARCH} %{SIZE}\n]' package_name.rpm
```

{{% alert title="注意" %}}
_`--queryformat`_ 是一个格式字符串，可用于获取包的特定信息。
可获取的信息来自 rpm -qip 命令。
{{% /alert %}}

### 检查包的内容

要检查包的内容，请使用以下命令：

```bash
rpm -qlp package_name.rpm
```

该命令会列出包中包含的所有文件。

### 调试脚本

要调试 post/pre 安装／卸载脚本，请使用以下命令：

```bash
rpm -qp --scripts package_name.rpm
```

该命令会打印脚本的内容。

### 检查依赖

要检查包的依赖，请使用以下命令：

```bash
rpm -qp --requires package_name.rpm
```

### 列出依赖某个特定包的包

要列出依赖某个特定包的包，请使用以下命令：

```bash
rpm -q --whatrequires package_name.rpm
```

### 调试安装问题

如果你在安装 RPM 包时遇到问题，
可以使用 `-vv`（非常详细）选项获取详细输出：

```bash
rpm -ivvh package_name.rpm
```

或者对已安装的包：

```bash
rpm -Uvvh package_name.rpm
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
