+++
title = "3 Barcode Scanner"
date = 2026-09-25T21:31:08+08:00
weight = 3
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/barcode-scanner/](https://tauri.app/plugin/barcode-scanner/)

让你的移动应用使用摄像头扫描二维码、EAN-13 以及其他类型的条形码。

## 支持的平台

| 平台 | 支持程度 | 说明 |
| --- | --- | --- |
| Windows | 不支持 |  |
| Linux | 不支持 |  |
| macOS | 不支持 |  |
| Android | 完整支持 |  |
| iOS | 完整支持 |  |

## 设置

{{< tabpane text=true persist=disabled >}}
{{% tab header="自动" %}}

使用你的项目包管理器添加依赖：

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm run tauri add barcode-scanner
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add barcode-scanner
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add barcode-scanner
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add barcode-scanner
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add barcode-scanner
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add barcode-scanner
```

{{% /tab %}}

{{< /tabpane >}}
{{% /tab %}}

{{% tab header="手动" %}}

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-barcode-scanner --target 'cfg(any(target_os = "android", target_os = "ios"))'
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .setup(|app| {
               #[cfg(mobile)]
               app.handle().plugin(tauri_plugin_barcode_scanner::init());
               Ok(())
           })
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-barcode-scanner
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-barcode-scanner
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-barcode-scanner
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-barcode-scanner
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-barcode-scanner
```

{{% /tab %}}

{{< /tabpane >}}
{{% /tab %}}

{{< /tabpane >}}
## 配置

在 iOS 上，barcode scanner 插件需要 `NSCameraUsageDescription` 信息属性列表值，它应当说明你的应用为什么需要使用摄像头。

在 `src-tauri/Info.ios.plist` 文件中加入以下片段：

```xml
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
	<dict>
		<key>NSCameraUsageDescription</key>
		<string>Read QR codes</string>
	</dict>
</plist>
```

## 用法

barcode scanner 插件在 JavaScript 中可用。

```javascript
import { scan, Format } from '@tauri-apps/plugin-barcode-scanner';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { scan, Format } = window.__TAURI__.barcodeScanner;

// `windowed: true` 实际上会把 webview 设为透明，
// 而不是为摄像头打开一个独立的视图。
// 请确保你的用户界面已准备好用透明元素展示其下方的内容
scan({ windowed: true, formats: [Format.QRCode] });
```

## 权限

默认情况下，所有有潜在危险的插件命令和作用域都被阻止，无法访问。你必须在 `capabilities` 配置中修改权限才能启用它们。

更多信息请参阅[能力概述](../../security/4-capabilities/)，以及[使用插件权限的分步指南](../../learn/security/1-usingpluginpermissions/)。

```json
{
  "$schema": "../gen/schemas/mobile-schema.json",
  "identifier": "mobile-capability",
  "windows": ["main"],
  "platforms": ["iOS", "android"],
  "permissions": ["barcode-scanner:allow-scan", "barcode-scanner:allow-cancel"]
}
```
