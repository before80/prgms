+++
title = "22 Process"
date = 2026-09-25T21:31:08+08:00
weight = 22
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/process/](https://tauri.app/plugin/process/)

访问当前进程。要启动子进程，请参阅 [shell](../23-shell/) 插件。

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
npm run tauri add process
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add process
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add process
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add process
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add process
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add process
```

{{% /tab %}}

{{< /tabpane >}}

### 手动

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-process
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_process::init())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-process
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-process
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-process
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-process
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-process
```

{{% /tab %}}

{{< /tabpane >}}


## 用法

process 插件在 JavaScript 和 Rust 中都可以使用。

**语言**

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```javascript
import { exit, relaunch } from '@tauri-apps/plugin-process';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { exit, relaunch } = window.__TAURI__.process;

// 以给定的状态码退出应用
await exit(0);

// 重启应用
await relaunch();
```

{{% /tab %}}

{{% tab header="Rust" %}}

注意 `app` 是 [`AppHandle`](https://docs.rs/tauri/2.0.0/tauri/struct.AppHandle.html) 的实例。

```rust
app.exit(0);

// 重启应用
app.restart();
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
    "process:default"
  ]
}
```
