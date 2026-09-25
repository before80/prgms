+++
title = "19 OS Information"
date = 2026-09-25T21:31:08+08:00
weight = 19
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/os-info/](https://tauri.app/plugin/os-info/)

读取操作系统信息。

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
npm run tauri add os
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add os
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add os
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add os
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add os
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add os
```

{{% /tab %}}

{{< /tabpane >}}

{{% /tab %}}

{{% tab header="手动" %}}

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-os
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_os::init())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-os
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-os
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-os
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-os
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-os
```

{{% /tab %}}

{{< /tabpane >}}

{{% /tab %}}

{{< /tabpane >}}

## 用法

用这个插件你可以查询当前操作系统的多种信息。所有可用函数见 [JavaScript API](https://tauri.app/reference/javascript/os/) 或 [Rust API](https://docs.rs/tauri-plugin-os/) 参考。

#### 示例：操作系统平台

`platform` 返回描述当前所用操作系统的字符串。该值在编译期确定。可能的取值有 `linux`、`macos`、`ios`、`freebsd`、`dragonfly`、`netbsd`、`openbsd`、`solaris`、`android`、`windows`。

**语言**

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```javascript
import { platform } from '@tauri-apps/plugin-os';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { platform } = window.__TAURI__.os;

const currentPlatform = platform();
console.log(currentPlatform);
// 会在控制台打印 "windows"
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
println!("Platform: {}", platform);
// 会在终端打印 "windows"
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
    "os:default"
  ]
}
```
