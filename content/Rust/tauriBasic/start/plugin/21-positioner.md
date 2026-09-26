+++
title = "21 Positioner"
date = 2026-09-25T21:31:08+08:00
weight = 21
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/positioner/](https://tauri.app/plugin/positioner/)

把窗口放到众所周知的位置。

## 支持的平台

| 平台 | 支持程度 | 说明 |
| --- | --- | --- |
| Windows | 完整支持 |  |
| Linux | 完整支持 |  |
| macOS | 完整支持 |  |
| Android | 不支持 |  |
| iOS | 不支持 |  |

## 设置

### 自动

使用你的项目包管理器添加依赖：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri add positioner
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add positioner
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add positioner
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add positioner
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add positioner
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add positioner
```

{{% /tab %}}

{{< /tabpane >}}

### 手动

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-positioner
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_positioner::init())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-positioner
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-positioner
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-positioner
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-positioner
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-positioner
```

{{% /tab %}}

{{< /tabpane >}}


## 用法

该插件的 API 可以通过 JavaScript 端绑定使用：

```javascript
import { moveWindow, Position } from '@tauri-apps/plugin-positioner';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { moveWindow, Position } = window.__TAURI__.positioner;

moveWindow(Position.TopRight);
```

你也可以直接在 Rust 中导入并使用 Window trait 扩展：

```rust
use tauri_plugin_positioner::{WindowExt, Position};

let mut win = app.get_webview_window("main").unwrap();
let _ = win.as_ref().window().move_window(Position::TopRight);
```

## 权限

默认情况下，所有有潜在危险的插件命令和作用域都被阻止，无法访问。你必须在 `capabilities` 配置中修改权限才能启用它们。

更多信息请参阅[能力概述](../../security/4-capabilities/)，以及[使用插件权限的分步指南](../../learn/security/1-usingpluginpermissions/)。

```json
{
  "permissions": [
    ...,
    "positioner:default"
  ]
}
```
