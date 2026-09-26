+++
title = "10 Geolocation"
date = 2026-09-25T21:31:08+08:00
weight = 10
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/geolocation/](https://tauri.app/plugin/geolocation/)

获取并跟踪设备当前位置，包括高度、方向与速度信息（如果可用）。

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
npm run tauri add geolocation
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add geolocation
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add geolocation
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add geolocation
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add geolocation
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add geolocation
```

{{% /tab %}}

{{< /tabpane >}}

### 手动

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-geolocation
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_geolocation::init())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-geolocation
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-geolocation
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-geolocation
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-geolocation
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-geolocation
```

{{% /tab %}}

{{< /tabpane >}}


## 用法

geolocation 插件在 JavaScript 中可用。

```javascript
import {
  checkPermissions,
  requestPermissions,
  getCurrentPosition,
  watchPosition,
} from '@tauri-apps/plugin-geolocation';

let permissions = await checkPermissions();
if (
  permissions.location === 'prompt' ||
  permissions.location === 'prompt-with-rationale'
) {
  permissions = await requestPermissions(['location']);
}

if (permissions.location === 'granted') {
  const pos = await getCurrentPosition();

  await watchPosition(
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 },
    (pos) => {
      console.log(pos);
    }
  );
}
```

## 权限

默认情况下，所有有潜在危险的插件命令和作用域都被阻止，无法访问。你必须在 `capabilities` 配置中修改权限才能启用它们。

更多信息请参阅[能力概述](../../security/4-capabilities/)，以及[使用插件权限的分步指南](../../learn/security/1-usingpluginpermissions/)。

```json
{
  "permissions": [
    ...,
    "geolocation:default"
  ]
}
```
