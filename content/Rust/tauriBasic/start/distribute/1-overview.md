+++
title = "1 分发概述"
date = 2026-09-25T21:31:08+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/distribute/](https://tauri.app/distribute/)

Tauri 提供了你分发应用所需的工具，无论是分发到各平台应用商店，还是作为平台特定的安装包。

## 构建

Tauri 直接通过其 CLI 的 `build`、`android build` 和 `ios build` 命令构建你的应用。

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

关于每种打包格式可用的配置选项以及如何把它们分发给用户，请参阅[分发](#分发)一节。

{{% alert title="注意" %}}
大多数平台都要求代码签名。更多信息请参阅[签名](#签名)一节。
{{% /alert %}}

### 打包

默认情况下，`build` 命令会自动按所配置的格式打包你的应用。

如果你需要进一步自定义平台包的生成方式，可以把构建与打包步骤拆开：

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri build -- --no-bundle
# 为 macOS App Store 之外的分发打包
npm run tauri bundle -- --bundles app,dmg
# 为 App Store 分发打包
npm run tauri bundle -- --bundles app --config src-tauri/tauri.appstore.conf.json
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri build --no-bundle
# 为 macOS App Store 之外的分发打包
yarn tauri bundle --bundles app,dmg
# 为 App Store 分发打包
yarn tauri bundle --bundles app --config src-tauri/tauri.appstore.conf.json
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri build --no-bundle
# 为 macOS App Store 之外的分发打包
pnpm tauri bundle --bundles app,dmg
# 为 App Store 分发打包
pnpm tauri bundle --bundles app --config src-tauri/tauri.appstore.conf.json
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri build --no-bundle
# 为 macOS App Store 之外的分发打包
deno task tauri bundle --bundles app,dmg
# 为 App Store 分发打包
deno task tauri bundle --bundles app --config src-tauri/tauri.appstore.conf.json
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri build --no-bundle
# 为 macOS App Store 之外的分发打包
bun tauri bundle --bundles app,dmg
# 为 App Store 分发打包
bun tauri bundle --bundles app --config src-tauri/tauri.appstore.conf.json
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri build --no-bundle
# 为 macOS App Store 之外的分发打包
cargo tauri bundle --bundles app,dmg
# 为 App Store 分发打包
cargo tauri bundle --bundles app --config src-tauri/tauri.appstore.conf.json
```

{{% /tab %}}

{{< /tabpane >}}

## 版本管理

你的应用版本可以在 [`tauri.conf.json > version`](https://tauri.app/reference/config/#version) 配置项中定义，
这也是管理应用版本的推荐方式。如果没有设置该配置项，
Tauri 会改用 `src-tauri/Cargo.toml` 文件中的 `package > version` 值。

{{% alert title="注意" %}}
某些平台对版本字符串有一些限制和特殊情况。
更多信息请参阅各平台的分发文档页面。
{{% /alert %}}

## 签名

代码签名通过对应用的可执行文件和打包产物施加数字签名来增强应用的安全性，验证你作为应用提供者的身份。

大多数平台都要求签名。更多信息请参阅各平台的文档。

- [macOS](../sign/1-macos/)：macOS 应用的代码签名与公证
- [Windows](../sign/3-windows/)：为 Windows 安装包进行代码签名
- [Linux](../sign/4-linux/)：为 Linux 软件包进行代码签名
- [Android](../sign/5-android/)：Android 的代码签名
- [iOS](../sign/2-ios/)：iOS 的代码签名

## 分发

了解如何为各平台分发你的应用。

### Linux

在 Linux 上，你可以使用 Debian 包、Snap、AppImage、Flatpak、RPM 或 Arch 用户仓库（AUR）格式分发应用。

- [AppImage](../2-appimage/)：以 AppImage 分发
- [AUR](../5-aur/)：发布到 Arch 用户仓库
- [Debian](../6-debian/)：以 Debian 包分发
- [RPM](../13-rpm/)：以 RPM 包分发
- [Snapcraft](../14-snapcraft/)：在 Snapcraft.io 上分发

[代码签名](../sign/4-linux/)

### macOS

在 macOS 上，你既可以直接把应用分发到 App Store，也可以提供 DMG 安装包作为直接下载。
两种方式都需要代码签名，而在 App Store 之外分发还需要公证。

- [App Bundle](../10-macosapplicationbundle/)：以 App Bundle 形式分发 macOS 应用
- [App Store](../3-appstore/)：把 iOS 和 macOS 应用分发到 App Store
- [DMG](../8-dmg/)：以 Apple Disk Image 形式分发 macOS 应用

[代码签名与公证](../sign/1-macos/)

### Windows

了解如何分发到 Microsoft Store，或配置 Windows 安装包。

- [Microsoft Store](../12-microsoftstore/)：把 Windows 应用分发到 Microsoft Store
- [Windows Installer](../15-windowsinstaller/)：分发 Windows 安装包

[代码签名](../sign/3-windows/)

### Android

把你的 Android 应用分发到 Google Play。

- [Google Play](../9-googleplay/)：把 Android 应用分发到 Google Play

[代码签名](../sign/5-android/)

### iOS

了解如何把你的应用上传到 App Store。

- [App Store](../3-appstore/)：把 iOS 和 macOS 应用分发到 App Store

[代码签名](../sign/2-ios/)

### 云服务

把你的应用分发到可以全球分发应用并开箱支持自动更新的云服务。

- [CrabNebula Cloud](../4-crabnebulacloud/)：使用 CrabNebula 分发你的应用
