+++
title = "9 Google Play"
date = 2026-09-25T21:31:08+08:00
weight = 9
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/distribute/google-play/](https://tauri.app/distribute/google-play/)

Google Play 是 Google 维护的 Android 应用分发服务。

本指南涵盖在 Google Play 上发布 Android 应用的要求。

{{% alert title="注意" %}}
Tauri 底层使用 Android Studio 项目，因此构建和发布 Android 应用的任何官方做法同样适用于你的应用。
更多信息请参阅[官方文档](https://developer.android.com/distribute)。
{{% /alert %}}

## 要求

要在 Play Store 中分发 Android 应用，你必须创建一个 [Play Console](https://play.google.com/console/developers) 开发者账号。

此外，你还必须设置[代码签名](../sign/5-android/)。

更多信息请参阅[发布检查清单](https://play.google.com/console/about/guides/releasewithconfidence/)。

## 更换应用图标

运行 `tauri android init` 设置好 Android Studio 项目之后，你可以使用 `tauri icon` 命令更新应用图标。

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri icon /path/to/app-icon.png
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri icon /path/to/app-icon.png
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri icon /path/to/app-icon.png
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri icon /path/to/app-icon.png
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri icon /path/to/app-icon.png
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri icon /path/to/app-icon.png
```

{{% /tab %}}

{{< /tabpane >}}

## 配置

创建 Play Console 开发者账号之后，你需要在 Google [Play Console](https://play.google.com/console/developers) 网站上注册你的应用。它会引导你完成所有必需的表格和设置任务。

## 构建

你可以运行以下命令构建一个 Android App Bundle（AAB）以上传到 Google Play：

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri android build -- --aab
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri android build --aab
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri android build --aab
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri android build --aab
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri android build --aab
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri android build --aab
```

{{% /tab %}}

{{< /tabpane >}}

Tauri 会从 [`tauri.conf.json > version`](https://tauri.app/reference/config/#version) 中定义的值推导版本号（`versionCode = major*1000000 + minor*1000 + patch`）。
如果你需要不同的版本号方案（例如顺序编号），可以在 [`tauri.conf.json > bundle > android > versionCode`](https://tauri.app/reference/config/#versioncode) 配置中设置自定义版本号：

```json
{
  "bundle": {
    "android": {
      "versionCode": 100
    }
  }
}
```

### 构建 APK

AAB 格式是上传到 Google Play 的推荐打包格式，但也可以生成可用于测试或在商店之外分发的 APK。
要为你的应用编译 APK，你可以使用 `--apk` 参数：

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri android build -- --apk
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri android build --apk
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri android build --apk
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri android build --apk
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri android build --apk
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri android build --apk
```

{{% /tab %}}

{{< /tabpane >}}

### 架构选择

默认情况下，Tauri 会为所有受支持的架构（aarch64、armv7、i686 和 x86_64）构建你的应用。
要只为部分目标编译，你可以使用 `--target` 参数：

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri android build -- --aab --target aarch64 --target armv7
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri android build --aab --target aarch64 --target armv7
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri android build --aab --target aarch64 --target armv7
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri android build --aab --target aarch64 --target armv7
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri android build --aab --target aarch64 --target armv7
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri android build --aab --target aarch64 --target armv7
```

{{% /tab %}}

{{< /tabpane >}}

### 按架构拆分打包

默认情况下生成的 AAB 与 APK 是通用的，包含所有受支持的目标。
要为每个目标生成单独的包，请使用 `--split-per-abi` 参数。

{{% alert title="注意" %}}
这只对测试或在 Google Play 之外分发有用，因为它减小了文件体积但上传起来不太方便。Google Play 会替你处理受支持的架构。
{{% /alert %}}

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri android build -- --apk --split-per-abi
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri android build --apk --split-per-abi
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri android build --apk --split-per-abi
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri android build --apk --split-per-abi
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri android build --apk --split-per-abi
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri android build --apk --split-per-abi
```

{{% /tab %}}

{{< /tabpane >}}

### 修改最低支持的 Android 版本

Tauri 应用最低支持的 Android 版本是 Android 7.0（代号 Nougat，SDK 24）。

有一些技巧可以在仍支持旧系统的同时使用更新的 Android API。
更多信息请参阅 [Android 文档](https://developer.android.com/training/basics/supporting-devices/platforms#version-codes)。

如果你的应用必须在更新的 Android 版本上运行，你可以配置 [`tauri.conf.json > bundle > android > minSdkVersion`](https://tauri.app/reference/config/#minsdkversion)：

```json
{
  "bundle": {
    "android": {
      "minSdkVersion": 28
    }
  }
}
```

## 上传

构建好应用并生成 Android App Bundle 文件之后（该文件位于 `gen/android/app/build/outputs/bundle/universalRelease/app-universal-release.aab`），
你现在可以在 Google Play Console 中创建新发布并上传它。

首次上传必须在网站上手动完成，以便它验证你的应用签名和 bundle 标识符。
Tauri 目前没有提供自动化创建 Android 发布的方式——那需要借助 [Google Play Developer API](https://developers.google.com/android-publisher/api-ref/rest)，相关工作仍在进行中。
