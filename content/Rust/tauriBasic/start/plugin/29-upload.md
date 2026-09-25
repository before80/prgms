+++
title = "29 Upload"
date = 2026-09-25T21:31:08+08:00
weight = 29
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/upload/](https://tauri.app/plugin/upload/)

通过 HTTP 上传与下载文件。

## 支持的平台

| 平台 | 支持程度 | 说明 |
| --- | --- | --- |
| Windows | 完整支持 |  |
| Linux | 完整支持 |  |
| macOS | 完整支持 |  |
| Android | 完整支持 |  |
| iOS | 完整支持 |  |

## 设置

{{< tabpane text=true persist=disabled >}}

{{% tab header="自动" %}}

使用你的项目包管理器添加依赖：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri add upload
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add upload
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add upload
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add upload
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add upload
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add upload
```

{{% /tab %}}

{{< /tabpane >}}

{{% /tab %}}

{{% tab header="手动" %}}

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-upload
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_upload::init())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-upload
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-upload
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-upload
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-upload
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-upload
```

{{% /tab %}}

{{< /tabpane >}}

{{% /tab %}}

{{< /tabpane >}}

## 用法

完成插件的注册与设置之后，你可以通过 JavaScript 端绑定访问它的所有 API。

下面是一个使用该插件上传和下载文件的示例：

```javascript
import { upload } from '@tauri-apps/plugin-upload';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { upload } = window.__TAURI__.upload;

upload(
  'https://example.com/file-upload',
  './path/to/my/file.txt',
  ({ progress, total }) =>
    console.log(`Uploaded ${progress} of ${total} bytes`), // 上传进度回调
  { 'Content-Type': 'text/plain' } // 可选：随请求发送的头
);
```

```javascript
import { download } from '@tauri-apps/plugin-upload';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { download } = window.__TAURI__.upload;

download(
  'https://example.com/file-download-link',
  './path/to/save/my/file.txt',
  ({ progress, total }) =>
    console.log(`Downloaded ${progress} of ${total} bytes`), // 下载进度回调
  { 'Content-Type': 'text/plain' } // 可选：随请求发送的头
);
```

## 权限

默认情况下，所有有潜在危险的插件命令和作用域都被阻止，无法访问。你必须在 `capabilities` 配置中修改权限才能启用它们。

更多信息请参阅[能力概述](../../security/4-capabilities/)，以及[使用插件权限的分步指南](../../learn/security/1-usingpluginpermissions/)。

```json
{
  "permissions": [
    ...,
    "upload:default"
  ]
}
```
