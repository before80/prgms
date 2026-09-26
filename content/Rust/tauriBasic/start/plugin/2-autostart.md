+++
title = "2 Autostart"
date = 2026-09-25T21:31:08+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/autostart/](https://tauri.app/plugin/autostart/)

在系统启动时自动运行你的应用。

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
npm run tauri add autostart
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add autostart
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add autostart
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add autostart
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add autostart
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add autostart
```

{{% /tab %}}

{{< /tabpane >}}

### 手动

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-autostart
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_autostart::init())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-autostart
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-autostart
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-autostart
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-autostart
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-autostart
```

{{% /tab %}}

{{< /tabpane >}}


## 用法

autostart 插件在 JavaScript 和 Rust 中都可以使用。

**语言**

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```javascript
import { enable, isEnabled, disable } from '@tauri-apps/plugin-autostart';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { enable, isEnabled, disable } = window.__TAURI__.autostart;

// 启用自启动
await enable();
// 检查启用状态
console.log(`registered for autostart? ${await isEnabled()}`);
// 禁用自启动
disable();
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            #[cfg(desktop)]
            {
                use tauri_plugin_autostart::MacosLauncher;
                use tauri_plugin_autostart::ManagerExt;

                app.handle().plugin(tauri_plugin_autostart::init(
                    MacosLauncher::LaunchAgent,
                    Some(vec!["--flag1", "--flag2"]),
                ));

                // 获取自启动管理器
                let autostart_manager = app.autolaunch();
                // 启用自启动
                let _ = autostart_manager.enable();
                // 检查启用状态
                println!("registered for autostart? {}", autostart_manager.is_enabled().unwrap());
                // 禁用自启动
                let _ = autostart_manager.disable();
            }
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
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
    "autostart:allow-enable",
    "autostart:allow-disable",
    "autostart:allow-is-enabled"
  ]
}
```
