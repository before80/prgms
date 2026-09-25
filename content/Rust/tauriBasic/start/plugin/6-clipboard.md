+++
title = "6 Clipboard"
date = 2026-09-25T21:31:08+08:00
weight = 6
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/clipboard/](https://tauri.app/plugin/clipboard/)

使用剪贴板插件读写系统剪贴板。

## 支持的平台

| 平台 | 支持程度 | 说明 |
| --- | --- | --- |
| Windows | 完整支持 |  |
| Linux | 完整支持 |  |
| macOS | 完整支持 |  |
| Android | 部分支持 |  |
| iOS | 部分支持 |  |

## 设置

安装剪贴板插件即可开始。

**安装方式**

{{< tabpane text=true persist=disabled >}}
{{% tab header="自动" %}}

使用你的项目包管理器添加依赖：

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm run tauri add clipboard-manager
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add clipboard-manager
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add clipboard-manager
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add clipboard-manager
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add clipboard-manager
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add clipboard-manager
```

{{% /tab %}}

{{< /tabpane >}}
{{% /tab %}}

{{% tab header="手动" %}}

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-clipboard-manager
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_clipboard_manager::init())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 如果你想在 JavaScript 中管理剪贴板，还需要安装 npm 包：

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-clipboard-manager
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-clipboard-manager
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-clipboard-manager
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-clipboard-manager
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-clipboard-manager
```

{{% /tab %}}

{{< /tabpane >}}
{{% /tab %}}

{{< /tabpane >}}
## 用法

剪贴板插件在 JavaScript 和 Rust 中都可以使用。

**语言**

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```javascript
import { writeText, readText } from '@tauri-apps/plugin-clipboard-manager';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { writeText, readText } = window.__TAURI__.clipboardManager;

// 把内容写入剪贴板
await writeText('Tauri is awesome!');

// 从剪贴板读取内容
const content = await readText();
console.log(content);
// 会在控制台打印 "Tauri is awesome!"
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust

app.clipboard().write_text("Tauri is awesome!".to_string()).unwrap();

// 从剪贴板读取内容
let content = app.clipboard().read_text();
println!("{:?}", content.unwrap());
// 会在终端打印 "Tauri is awesome!"


```

{{% /tab %}}

{{< /tabpane >}}