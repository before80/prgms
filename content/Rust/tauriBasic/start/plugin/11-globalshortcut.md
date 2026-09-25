+++
title = "11 Global Shortcut"
date = 2026-09-25T21:31:08+08:00
weight = 11
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/global-shortcut/](https://tauri.app/plugin/global-shortcut/)

注册全局快捷键。

## 支持的平台

| 平台 | 支持程度 | 说明 |
| --- | --- | --- |
| Windows | 完整支持 |  |
| Linux | 完整支持 |  |
| macOS | 完整支持 |  |
| Android | 不支持 |  |
| iOS | 不支持 |  |

## 设置

{{< tabpane text=true persist=disabled >}}

{{% tab header="自动" %}}

使用你的项目包管理器添加依赖：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri add global-shortcut
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add global-shortcut
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add global-shortcut
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add global-shortcut
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add global-shortcut
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add global-shortcut
```

{{% /tab %}}

{{< /tabpane >}}

{{% /tab %}}

{{% tab header="手动" %}}

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-global-shortcut
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_global_shortcut::init())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-global-shortcut
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-global-shortcut
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-global-shortcut
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-global-shortcut
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-global-shortcut
```

{{% /tab %}}

{{< /tabpane >}}

{{% /tab %}}

{{< /tabpane >}}

## 用法

global-shortcut 插件在 JavaScript 和 Rust 中都可以使用。

**语言**

{{< tabpane text=true persist=disabled >}}

{{% tab header="JavaScript" %}}

```javascript
import { register } from '@tauri-apps/plugin-global-shortcut';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { register } = window.__TAURI__.globalShortcut;

await register('CommandOrControl+Shift+C', () => {
  console.log('Shortcut triggered');
});
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            #[cfg(desktop)]
            {
                use tauri_plugin_global_shortcut::{Code, GlobalShortcutExt, Modifiers, Shortcut, ShortcutState};

                let ctrl_n_shortcut = Shortcut::new(Some(Modifiers::CONTROL), Code::KeyN);
                app.handle().plugin(
                    tauri_plugin_global_shortcut::Builder::new().with_handler(move |_app, shortcut, event| {
                        println!("{:?}", shortcut);
                        if shortcut == &ctrl_n_shortcut {
                            match event.state() {
                              ShortcutState::Pressed => {
                                println!("Ctrl-N Pressed!");
                              }
                              ShortcutState::Released => {
                                println!("Ctrl-N Released!");
                              }
                            }
                        }
                    })
                    .build(),
                )?;

                app.global_shortcut().register(ctrl_n_shortcut)?;
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
    "global-shortcut:default"
  ]
}
```
