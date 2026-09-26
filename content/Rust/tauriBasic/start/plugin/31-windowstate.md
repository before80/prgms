+++
title = "31 Window State"
date = 2026-09-25T21:31:08+08:00
weight = 31
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/window-state/](https://tauri.app/plugin/window-state/)

保存并恢复窗口位置与尺寸。

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
npm run tauri add window-state
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add window-state
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add window-state
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add window-state
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add window-state
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add window-state
```

{{% /tab %}}

{{< /tabpane >}}

### 手动

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-window-state
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_window_state::init())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-window-state
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-window-state
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-window-state
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-window-state
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-window-state
```

{{% /tab %}}

{{< /tabpane >}}


## 用法

加入 window-state 插件后，所有窗口都会在应用关闭时记住自己的状态，并在下次启动时恢复到之前的状态。

你也可以在 JavaScript 和 Rust 中使用 window-state 插件。

{{% alert title="提示" %}}
状态恢复发生在窗口创建之后。因此为防止窗口闪烁，你可以在创建窗口时把 `visible` 设为 `false`，插件会在恢复状态后显示该窗口。
{{% /alert %}}

### JavaScript

你可以用 `saveWindowState` 手动保存窗口状态：

```javascript
import { saveWindowState, StateFlags } from '@tauri-apps/plugin-window-state';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { saveWindowState, StateFlags } = window.__TAURI__.windowState;

saveWindowState(StateFlags.ALL);
```

同样，你也可以手动从磁盘恢复窗口状态：

```javascript
import {
  restoreStateCurrent,
  StateFlags,
} from '@tauri-apps/plugin-window-state';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { restoreStateCurrent, StateFlags } = window.__TAURI__.windowState;

restoreStateCurrent(StateFlags.ALL);
```

### Rust

你可以使用 `AppHandleExt` trait 暴露的 `save_window_state()` 方法：

```rust
use tauri_plugin_window_state::{AppHandleExt, StateFlags};

// `tauri::AppHandle` 现在多了以下方法
app.save_window_state(StateFlags::all()); // 会把所有打开窗口的状态保存到磁盘
```

同样，你也可以用 `WindowExt` trait 暴露的 `restore_state()` 方法手动从磁盘恢复窗口状态：

```rust
use tauri_plugin_window_state::{WindowExt, StateFlags};

// 所有 `Window` 类型现在多了以下方法
window.restore_state(StateFlags::all()); // 会从磁盘恢复窗口状态
```

## 权限

默认情况下，所有有潜在危险的插件命令和作用域都被阻止，无法访问。你必须在 `capabilities` 配置中修改权限才能启用它们。

更多信息请参阅[能力概述](../../security/4-capabilities/)，以及[使用插件权限的分步指南](../../learn/security/1-usingpluginpermissions/)。

```json
{
  "permissions": [
    ...,
    "window-state:default"
  ]
}
```
