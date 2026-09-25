+++
title = "12 Microsoft Store"
date = 2026-09-25T21:31:08+08:00
weight = 12
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/distribute/microsoft-store/](https://tauri.app/distribute/microsoft-store/)

Microsoft Store 是 Microsoft 运营的 Windows 应用商店。

本指南只涵盖把 Windows 应用直接分发到 Microsoft Store 的细节。
关于 Windows 安装包分发选项与配置的更多信息，请参阅 [Windows 安装包指南](../15-windowsinstaller/)。

## 要求

要在 Microsoft Store 上发布应用，你必须拥有 Microsoft 账号，
并以个人或公司身份[注册](https://learn.microsoft.com/en-us/windows/apps/get-started/sign-up)为开发者。

## 更换应用图标

Tauri CLI 可以生成你的应用所需的所有图标，包括 Microsoft Store 图标。
使用 `tauri icon` 命令从单个 PNG 或 SVG 源生成应用图标：

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

用你的 Microsoft 账号注册为开发者之后，你需要在 [应用与游戏](https://partner.microsoft.com/en-us/dashboard/apps-and-games/overview)页面注册你的应用。
点击 `New Product`，选择 `EXE or MSI app`，并为你的应用预留一个唯一名称。

## 构建与上传

目前 Tauri 只生成 [EXE 与 MSI](../15-windowsinstaller/) 安装包，因此你必须创建一个只链接到未打包应用的 Microsoft Store 应用。
Microsoft Store 中链接的安装包必须是离线的、[处理自动更新](../../plugin/28-updater/)并且[经过代码签名](../sign/3-windows/)。

更多信息请参阅[官方发布文档](https://learn.microsoft.com/en-us/windows/apps/publish/)。

### 离线安装包

通过 Microsoft Store 分发的 Windows 安装包必须使用[离线安装](../15-windowsinstaller/#离线安装包)的 Webview2 安装选项。

要只在为 Microsoft Store 打包时应用该安装包配置，你可以定义一个单独的 Tauri 配置文件：

```json
{
  "bundle": {
    "windows": {
      "webviewInstallMode": {
        "type": "offlineInstaller"
      }
    }
  }
}
```

然后在为 Microsoft Store 打包 Tauri 应用时，把该配置文件与主配置合并：

**包管理器**

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri build -- --no-bundle
npm run tauri bundle -- --config src-tauri/tauri.microsoftstore.conf.json
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri build --no-bundle
yarn tauri bundle --config src-tauri/tauri.microsoftstore.conf.json
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri build --no-bundle
pnpm tauri bundle --config src-tauri/tauri.microsoftstore.conf.json
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri build --no-bundle
deno task tauri bundle --config src-tauri/tauri.microsoftstore.conf.json
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri build --no-bundle
bun tauri bundle --config src-tauri/tauri.microsoftstore.conf.json
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri build --no-bundle
cargo tauri bundle --config src-tauri/tauri.microsoftstore.conf.json
```

{{% /tab %}}

{{< /tabpane >}}

当你在 CI/CD 中把应用上传到 Microsoft Store，同时又为在应用商店之外分发的 Windows 安装包保留单独配置时，这尤其有用。

### 静默安装

Microsoft Store 要求 Win32 安装包支持静默安装。如果你的安装包不能静默安装，
你的提交会被拒绝并报如下错误：

```
10.2.9.2 Security - Package Submissions | Win32 products must install silently.
```

在 Partner Center 注册安装包时，你必须提供[静默安装参数](https://learn.microsoft.com/en-us/windows/uwp/publish/msiexe/provide-package-details)，以便商店可以无人值守地运行它。Tauri 的 NSIS `-setup.exe` 安装包通过 `/S` 参数（注意是大写 `S`）静默安装：

```
MyApp_x64-setup.exe /S
```

在你的 Microsoft Store 产品的安装包参数中输入 `/S` 作为静默安装参数。
如果你改为分发 MSI 安装包，请使用标准的 `msiexec` 参数 `/quiet`。

### 发布者

你的应用[发布者](https://tauri.app/reference/config/#publisher)名称不能与应用产品名称相同。

如果没有设置发布者配置值，Tauri 会从你的 bundle 标识符的第二部分推导它。
由于发布者名称不能与产品名称相同，下面的配置是无效的：

```json
{
  "productName": "Example",
  "identifier": "com.example.app"
}
```

这种情况下你可以单独定义[发布者](https://tauri.app/reference/config/#publisher)值来修正这一冲突：

```json
{
  "productName": "Example",
  "identifier": "com.example.app",
  "bundle": {
    "publisher": "Example Inc."
  }
}
```

### 上传

为 Microsoft Store 构建好 Windows 安装包之后，你可以把它上传到你选择的分发服务，并在 Microsoft Store 网站的应用页面中链接它。
