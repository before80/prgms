+++
title = "4 能力"
date = 2026-09-25T21:31:08+08:00
weight = 4
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/security/capabilities/](https://tauri.app/security/capabilities/)

Tauri 为应用和插件开发者提供了能力（capabilities）系统，用于细粒度地启用并约束对运行在系统 WebView 中的应用前端所暴露的核心能力。

能力定义了哪些[权限](../2-permissions/)被授予或拒绝给哪些窗口或 webview。

能力可以影响多个窗口和 webview，这些窗口和 webview 也可以在多个能力中被引用。

{{% alert title="安全提示" %}}

如果一个窗口或 WebView 同时属于多个能力，实际上就合并了所有相关能力的安全边界与权限。

{{% /alert %}}

能力文件以 JSON 或 TOML 文件的形式定义在 `src-tauri/capabilities` 目录中。

推荐做法是使用独立文件，并在 `tauri.conf.json` 中只按标识符引用它们；不过也可以直接在 `capabilities` 字段中定义。

`capabilities` 目录中的所有能力默认自动启用。
一旦在 `tauri.conf.json` 中显式启用了能力，应用构建时就只会使用这些能力。

配置方案的完整参考请见[参考](https://tauri.app/reference/config/)部分。

下面的 JSON 示例定义了一个能力，允许主窗口使用核心插件的默认功能以及 `window.setTitle` API。

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    "core:path:default",
    "core:event:default",
    "core:window:default",
    "core:app:default",
    "core:resources:default",
    "core:menu:default",
    "core:tray:default",
    "core:window:allow-set-title"
  ]
}
```

这些片段属于 [Tauri 配置](../../develop/2-configurationfiles/#tauri-配置)配置文件的一部分。

这大概是最常见的配置方式：把各个能力内联，只按标识符引用权限。

这要求在 `capabilities` 目录中有定义良好的能力文件。

```json
{
  "app": {
    "security": {
      "capabilities": ["my-capability", "main-capability"]
    }
  }
}
```

内联能力可以与预定义能力混用。

```json
{
  "app": {
    "security": {
      "capabilities": [
        {
          "identifier": "my-capability",
          "description": "My application capability used for all windows",
          "windows": ["*"],
          "permissions": ["fs:default", "allow-home-read-extended"]
        },
        "my-second-capability"
      ]
    }
  }
}
```

默认情况下，你在应用中注册的所有命令
（通过
[`tauri::Builder::invoke_handler`](https://docs.rs/tauri/2.0.0/tauri/struct.Builder.html#method.invoke_handler)
函数）
都允许被应用的所有窗口和 webview 使用。
若要改变这一点，可以考虑使用
[`AppManifest::commands`](https://docs.rs/tauri-build/2.0.0/tauri_build/struct.AppManifest.html#method.commands)。

```rust
fn main() {
    tauri_build::try_build(
        tauri_build::Attributes::new()
            .app_manifest(tauri_build::AppManifest::new().commands(&["your_command"])),
    )
    .unwrap();
}
```

## 目标平台

通过定义 `platforms` 数组，能力可以是平台特定的。
默认情况下能力会应用于所有目标，但你可以选择 `linux`、`macOS`、`windows`、`iOS` 和 `android` 中的一部分。

例如一个用于桌面操作系统的能力。
注意它启用的是仅在桌面端可用的插件权限：

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "desktop-capability",
  "windows": ["main"],
  "platforms": ["linux", "macOS", "windows"],
  "permissions": ["global-shortcut:allow-register"]
}
```

再看一个用于移动端的能力示例。
注意它启用的是仅在移动端可用的插件权限：

```json
{
  "$schema": "../gen/schemas/mobile-schema.json",
  "identifier": "mobile-capability",
  "windows": ["main"],
  "platforms": ["iOS", "android"],
  "permissions": [
    "nfc:allow-scan",
    "biometric:allow-authenticate",
    "barcode-scanner:allow-scan"
  ]
}
```

## 远程 API 访问

默认情况下，API 只对随 Tauri 应用一起分发的打包代码可用。
若要允许远程来源访问某些 Tauri 命令，可以在能力配置文件中定义。

下面这个示例允许从 `tauri.app` 的所有子域扫描 NFC 标签并使用条码扫描器。

```json
{
  "$schema": "../gen/schemas/remote-schema.json",
  "identifier": "remote-tag-capability",
  "windows": ["main"],
  "remote": {
    "urls": ["https://*.tauri.app"]
  },
  "platforms": ["iOS", "android"],
  "permissions": ["nfc:allow-scan", "barcode-scanner:allow-scan"]
}
```

{{% alert title="警告" color="warning" %}}

在 Linux 和 Android 上，Tauri 无法区分来自内嵌 `<iframe>` 的请求和窗口自身的请求。

请非常谨慎地考虑是否使用此特性，并在该特性的参考部分进一步阅读你所针对操作系统的具体安全影响。

{{% /alert %}}

## 安全边界

_它能防御什么？_

取决于所配置的权限与能力，它可以：

- 把前端被攻破的影响降到最低
- 防止或减少本地系统接口与数据的（意外）暴露
- 防止或减少从前端到后端／系统的可能提权

_它**不能**防御什么？_

- 恶意或不安全的 Rust 代码
- 过于宽松的作用域与配置
- 命令实现中不正确的作用域检查
- 来自 Rust 代码的故意绕过
- 基本上，任何写在应用 rust 核心里的东西
- 系统 WebView 中的 0-day 或未修补的 1-day
- 供应链攻击或以其它方式被攻破的开发者系统

{{% alert title="安全提示" %}}

安全边界取决于窗口标签（**而不是标题**）。
我们建议只把窗口创建功能暴露给权限更高的窗口。

{{% /alert %}}

## Schema 文件

Tauri 会通过 `tauri-build` 生成包含你应用所有可用权限的 JSON schema，从而在你的 IDE 中提供自动补全。要使用 schema，请把配置文件（.json 或 .toml）中的 `$schema` 属性设为 `gen/schemas` 目录下某个平台特定的 schema。通常你会把它设为 `../gen/schemas/desktop-schema.json` 或 `../gen/schemas/mobile-schema.json`，不过你也可以为特定目标平台定义能力。

## 配置文件

一个示例 Tauri 应用目录结构的简化版本：

```sh
├── index.html
├── package.json
├── src/
├── src-tauri/
│   ├── Cargo.toml
│   ├── capabilities/
│   │  └── <identifier>.json/toml
│   ├── src/
│   ├── tauri.conf.json
```

所有内容都可以内联进 `tauri.conf.json`，但即使稍微复杂一点的配置也会让这个文件变得臃肿；这种做法的目标是尽可能把权限抽象出去，并且易于理解。

## 核心权限

所有核心权限的清单可以在[核心权限](https://tauri.app/reference/acl/core-permissions/)页面找到。
