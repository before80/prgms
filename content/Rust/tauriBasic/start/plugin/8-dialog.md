+++
title = "8 Dialog"
date = 2026-09-25T21:31:08+08:00
weight = 8
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/dialog/](https://tauri.app/plugin/dialog/)

用于打开、保存文件的原生系统对话框，以及消息对话框。

## 支持的平台

| 平台 | 支持程度 | 说明 |
| --- | --- | --- |
| Windows | 完整支持 |  |
| Linux | 完整支持 |  |
| macOS | 完整支持 |  |
| Android | 部分支持 |  |
| iOS | 部分支持 |  |

## 设置

### 自动

使用你的项目包管理器添加依赖：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri add dialog
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add dialog
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add dialog
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add dialog
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add dialog
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add dialog
```

{{% /tab %}}

{{< /tabpane >}}

### 手动

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-dialog
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_dialog::init())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-dialog
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-dialog
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-dialog
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-dialog
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-dialog
```

{{% /tab %}}

{{< /tabpane >}}


## 用法

dialog 插件在 JavaScript 和 Rust 中都可以使用。用法如下：

在 JavaScript 中：

- [创建 Yes/No 对话框](#创建-yesno-对话框)
- [创建 Ok/Cancel 对话框](#创建-okcancel-对话框)
- [创建消息对话框](#创建消息对话框)
- [打开文件选择对话框](#打开文件选择对话框)
- [保存到文件对话框](#保存到文件对话框)

在 Rust 中：

- [构建询问对话框](#构建询问对话框)
- [构建消息对话框](#构建消息对话框)
- [构建文件选择对话框](#构建文件选择对话框)

{{% alert title="注意" %}}
在 Linux、Windows 和 macOS 上，文件对话框 API 返回文件系统路径。

在 iOS 上返回 `file://<path>` URI。

在 Android 上返回 [content URI](https://developer.android.com/guide/topics/providers/content-provider-basics)。

[文件系统插件](../9-filesystem/)开箱即可处理任何路径格式。
{{% /alert %}}

### JavaScript

所有 [Dialog 选项](https://tauri.app/reference/javascript/dialog/)见 JavaScript API 参考。

#### 创建 Yes/No 对话框

显示一个带 `Yes` 和 `No` 按钮的询问对话框。

```javascript
import { ask } from '@tauri-apps/plugin-dialog';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { ask } = window.__TAURI__.dialog;

// 创建一个 Yes/No 对话框
const answer = await ask('This action cannot be reverted. Are you sure?', {
  title: 'Tauri',
  kind: 'warning',
});

console.log(answer);
// 会在控制台打印布尔值
```

#### 创建 Ok/Cancel 对话框

显示一个带 `Ok` 和 `Cancel` 按钮的询问对话框。

```javascript
import { confirm } from '@tauri-apps/plugin-dialog';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { confirm } = window.__TAURI__.dialog;

// 创建一个 Ok/Cancel 确认对话框
const confirmation = await confirm(
  'This action cannot be reverted. Are you sure?',
  { title: 'Tauri', kind: 'warning' }
);

console.log(confirmation);
// 会在控制台打印布尔值
```

#### 创建消息对话框

显示一个带 `Ok` 按钮的消息对话框。请记住，如果用户关闭对话框，它会返回 `false`。

```javascript
import { message } from '@tauri-apps/plugin-dialog';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { message } = window.__TAURI__.dialog;

// 显示消息
await message('File not found', { title: 'Tauri', kind: 'error' });
```

#### 打开文件选择对话框

打开文件／目录选择对话框。

`multiple` 选项控制对话框是否允许多选，`directory` 控制是否是目录选择。

```javascript
import { open } from '@tauri-apps/plugin-dialog';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { open } = window.__TAURI__.dialog;

// 打开一个对话框
const file = await open({
  multiple: false,
  directory: false,
});
console.log(file);
// 打印文件路径或 URI
```

#### 保存到文件对话框

打开文件／目录保存对话框。

```javascript
import { save } from '@tauri-apps/plugin-dialog';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { save } = window.__TAURI__.dialog;

// 提示保存一个扩展名为 .png 或 .jpeg 的 'My Filter'
const path = await save({
  filters: [
    {
      name: 'My Filter',
      extensions: ['png', 'jpeg'],
    },
  ],
});
console.log(path);
// 打印所选择的路径
```

---

### Rust

所有可用选项请参阅 [Rust API 参考](https://docs.rs/tauri-plugin-dialog/)。

#### 构建询问对话框

显示一个带 `Absolutely` 和 `Totally` 按钮的询问对话框。

```rust
use tauri_plugin_dialog::{DialogExt, MessageDialogButtons};

let answer = app.dialog()
        .message("Tauri is Awesome")
        .title("Tauri is Awesome")
        .buttons(MessageDialogButtons::OkCancelCustom("Absolutely", "Totally"))
        .blocking_show();
```

如果你需要非阻塞操作，可以改用 `show()`：

```rust
use tauri_plugin_dialog::{DialogExt, MessageDialogButtons};

app.dialog()
    .message("Tauri is Awesome")
    .title("Tauri is Awesome")
   .buttons(MessageDialogButtons::OkCancelCustom("Absolutely", "Totally"))
    .show(|result| match result {
        true => // 做点什么，
        false =>// 做点什么，
    });
```

#### 构建消息对话框

显示一个带 `Ok` 按钮的消息对话框。请记住，如果用户关闭对话框，它会返回 `false`。

```rust
use tauri_plugin_dialog::{DialogExt, MessageDialogKind};

let ans = app.dialog()
    .message("File not found")
    .kind(MessageDialogKind::Error)
    .title("Warning")
    .blocking_show();
```

如果你需要非阻塞操作，可以改用 `show()`：

```rust
use tauri_plugin_dialog::{DialogExt, MessageDialogButtons, MessageDialogKind};

app.dialog()
    .message("Tauri is Awesome")
    .kind(MessageDialogKind::Info)
    .title("Information")
    .buttons(MessageDialogButtons::OkCustom("Absolutely"))
    .show(|result| match result {
        true => // 做点什么，
        false => // 做点什么，
    });
```

#### 构建文件选择对话框

##### 选取文件

```rust
use tauri_plugin_dialog::DialogExt;

let file_path = app.dialog().file().blocking_pick_file();
// 返回 `Option` 类型的 file_path；如果用户关闭对话框则为 `None`
```

如果你需要非阻塞操作，可以改用 `pick_file()`：

```rust
use tauri_plugin_dialog::DialogExt;

app.dialog().file().pick_file(|file_path| {
    // 返回 `Option` 类型的 file_path；如果用户关闭对话框则为 `None`
    })
```

##### 保存文件

```rust
use tauri_plugin_dialog::DialogExt;

let file_path = app
    .dialog()
    .file()
    .add_filter("My Filter", &["png", "jpeg"])
    .blocking_save_file();
    // 在这里处理可选的文件路径
    // 如果用户关闭了对话框，文件路径为 `None`
```

或者：

```rust
use tauri_plugin_dialog::DialogExt;

app.dialog()
    .file()
    .add_filter("My Filter", &["png", "jpeg"])
    .pick_file(|file_path| {
        // 返回 `Option` 类型的 file_path；如果用户关闭了对话框则为 `None`
    });
```
