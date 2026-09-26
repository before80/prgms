+++
title = "16 NFC"
date = 2026-09-25T21:31:08+08:00
weight = 16
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/nfc/](https://tauri.app/plugin/nfc/)

在 Android 和 iOS 上读写 NFC 标签。

## 支持的平台

| 平台 | 支持程度 | 说明 |
| --- | --- | --- |
| Windows | 不支持 |  |
| Linux | 不支持 |  |
| macOS | 不支持 |  |
| Android | 完整支持 |  |
| iOS | 完整支持 |  |

## 设置

### 自动

使用你的项目包管理器添加依赖：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri add nfc
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add nfc
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add nfc
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add nfc
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add nfc
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add nfc
```

{{% /tab %}}

{{< /tabpane >}}

### 手动

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-nfc
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_nfc::init())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-nfc
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-nfc
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-nfc
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-nfc
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-nfc
```

{{% /tab %}}

{{< /tabpane >}}


## 用法

NFC 插件在 JavaScript 和 Rust 中都可以使用，让你可以扫描并写入 NFC 标签。

### 检查是否支持 NFC

并非每台移动设备都能扫描 NFC 标签，因此在使用扫描和写入 API 之前应当先检查可用性。

**语言**

{{< tabpane text=true persist=disabled >}}

{{% tab header="JavaScript" %}}

```javascript
import { isAvailable } from '@tauri-apps/plugin-nfc';

const canScanNfc = await isAvailable();
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
tauri::Builder::default()
  .setup(|app| {
    #[cfg(mobile)]
    {
      use tauri_plugin_nfc::NfcExt;

      app.handle().plugin(tauri_plugin_nfc::init());

      let can_scan_nfc = app.nfc().is_available()?;
    }
    Ok(())
  })
```

{{% /tab %}}

{{< /tabpane >}}

### 扫描 NFC 标签

该插件既可以扫描通用 NFC 标签，也可以扫描带 NDEF（NFC Data Exchange Format）消息的 NFC 标签——NDEF 是在 NFC 标签中封装带类型数据的标准格式。

**语言**

{{< tabpane text=true persist=disabled >}}

{{% tab header="JavaScript" %}}

```javascript
import { scan } from '@tauri-apps/plugin-nfc';

const scanType = {
  type: 'ndef', // 或 'tag'，
};

const options = {
  keepSessionAlive: false,
  // 配置 iOS 上 “Scan NFC” 对话框中显示的消息
  message: 'Scan a NFC tag',
  successMessage: 'NFC tag successfully scanned',
};

const tag = await scan(scanType, options);
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
tauri::Builder::default()
  .setup(|app| {
    #[cfg(mobile)]
    {
      use tauri_plugin_nfc::NfcExt;

      app.handle().plugin(tauri_plugin_nfc::init());

      let tag = app
        .nfc()
        .scan(tauri_plugin_nfc::ScanRequest {
            kind: tauri_plugin_nfc::ScanKind::Ndef {
                mime_type: None,
                uri: None,
                tech_list: None,
            },
            keep_session_alive: false,
        })?
        .tag;
    }
    Ok(())
  })
```

{{% /tab %}}

{{< /tabpane >}}

{{% alert title="注意" %}}
`keepSessionAlive` 选项可用于稍后直接写入所扫描到的 NFC 标签。

如果不提供该选项，会话会在下一次 `write()` 调用时重建，
这意味着应用会尝试重新扫描标签。
{{% /alert %}}

#### 过滤器

NFC 扫描器也可以按特定 URI 格式、MIME 类型或 NFC 标签技术过滤标签。
这种情况下，扫描只会检测到与所提供过滤器匹配的标签。

{{% alert title="注意" %}}
过滤仅在 Android 上可用，因此你应当始终检查所扫描 NFC 标签的内容。

MIME 类型区分大小写，必须使用小写字母。
{{% /alert %}}

**语言**

{{< tabpane text=true persist=disabled >}}

{{% tab header="JavaScript" %}}

```javascript
import { scan, TechKind } from '@tauri-apps/plugin-nfc';

const techLists = [
  // 捕获任何使用 NfcF 的标签
  [TechKind.NfcF],
  // 捕获所有带 NDEF 负载的 MIFARE Classic
  [TechKind.NfcA, TechKind.MifareClassic, TechKind.Ndef],
];

const tag = await scan({
  type: 'ndef', // 或 'tag'
  mimeType: 'text/plain',
  uri: {
    scheme: 'https',
    host: 'my.domain.com',
    pathPrefix: '/app',
  },
  techLists,
});
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
tauri::Builder::default()
  .setup(|app| {
    #[cfg(mobile)]
    {
      use tauri_plugin_nfc::NfcExt;

      app.handle().plugin(tauri_plugin_nfc::init());

      let tag = app
        .nfc()
        .scan(tauri_plugin_nfc::ScanRequest {
            kind: tauri_plugin_nfc::ScanKind::Ndef {
                mime_type: Some("text/plain".to_string()),
                uri: Some(tauri_plugin_nfc::UriFilter {
                  scheme: Some("https".to_string()),
                  host: Some("my.domain.com".to_string()),
                  path_prefix: Some("/app".to_string()),
                }),
                tech_list: Some(vec![
                  vec![tauri_plugin_nfc::TechKind::Ndef],
                ]),
            },
        })?
        .tag;
    }
    Ok(())
  })
```

{{% /tab %}}

{{< /tabpane >}}

### 写入 NFC 标签

`write` API 可用于向 NFC 标签写入负载。
如果没有以 `keepSessionAlive: true` 扫描到的标签，应用会先扫描一个 NFC 标签。

**语言**

{{< tabpane text=true persist=disabled >}}

{{% tab header="JavaScript" %}}

```javascript
import { write, textRecord, uriRecord } from '@tauri-apps/plugin-nfc';

const payload = [uriRecord('https://tauri.app'), textRecord('some payload')];

const options = {
  // 只有在没有保持存活的已扫描标签会话时才需要 kind
  // 其格式与传给 scan() 的参数相同
  kind: {
    type: 'ndef',
  },
  // 配置 iOS 上 “Scan NFC” 对话框中显示的消息
  message: 'Scan a NFC tag',
  successfulReadMessage: 'NFC tag successfully scanned',
  successMessage: 'NFC tag successfully written',
};

await write(payload, options);
```

{{% /tab %}}

{{% tab header="Rust" %}}

{{% alert title="警告" color="warning" %}}
Rust API 目前只提供写入 NFC 负载的底层接口。

该 API 很快会得到增强。
{{% /alert %}}

```rust
tauri::Builder::default()
  .setup(|app| {
    #[cfg(mobile)]
    {
      use tauri_plugin_nfc::NfcExt;

      app.handle().plugin(tauri_plugin_nfc::init());

      app
        .nfc()
        .write(vec![
          tauri_plugin_nfc::NfcRecord {
            format: tauri_plugin_nfc::NFCTypeNameFormat::NfcWellKnown,
            kind: vec![0x55], // URI 记录
            id: vec![],
            payload: vec![], // 在这里填入负载
          }
        ])?;
    }
    Ok(())
  })
```

{{% /tab %}}

{{< /tabpane >}}

## 权限

默认情况下，所有有潜在危险的插件命令和作用域都被阻止，无法访问。你必须在 `capabilities` 配置中修改权限才能启用它们。

更多信息请参阅[能力概述](../../security/4-capabilities/)，以及[使用插件权限的分步指南](../../learn/security/1-usingpluginpermissions/)。

```json
{
  "permissions": [
    ...,
    "nfc:default"
  ]
}
```
