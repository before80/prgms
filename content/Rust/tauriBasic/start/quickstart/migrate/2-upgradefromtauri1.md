+++
title = "2 从 Tauri 1.0 升级"
date = 2026-09-25T21:31:08+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/start/migrate/from-tauri-1/](https://tauri.app/start/migrate/from-tauri-1/)

本指南将带你把自己的 Tauri 1.0 应用升级到 Tauri 2.0。

## 为移动端做准备

Tauri 的移动端接口要求你的项目输出一个共享库。如果你打算让现有应用支持移动端，就必须修改 crate，使其在生成桌面端可执行文件的同时也生成这种产物。

1. 修改 Cargo 清单以生成库。追加以下内容块：

```toml
[lib]
name = "app_lib"
crate-type = ["staticlib", "cdylib", "rlib"]
```

2. 将 `src-tauri/src/main.rs` 重命名为 `src-tauri/src/lib.rs`。该文件将被桌面端和移动端目标共享。

3. 将 `lib.rs` 中 `main` 函数的签名改为如下形式：

```rust
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    // 你的代码写在这里
}
```

`tauri::mobile_entry_point` 宏会让你的函数能够在移动端执行。

4. 重新创建 `main.rs` 文件，在其中调用共享的 run 函数：

```rust
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
  app_lib::run();
}
```

## 自动迁移

{{% alert title="危险" color="warning" %}}

这个命令不能替代本指南！无论你是否选择使用该命令，都请阅读**整篇**文档。

{{% /alert %}}

Tauri v2 CLI 提供了 `migrate` 命令，可以自动完成大部分迁移流程，并帮助你完成剩余工作：

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm install @tauri-apps/cli@latest
npm run tauri migrate
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn upgrade @tauri-apps/cli@latest
yarn tauri migrate
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm update @tauri-apps/cli@latest
pnpm tauri migrate
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri migrate
```

{{% /tab %}}

{{< /tabpane >}}
在[命令行界面参考](https://tauri.app/reference/cli/#migrate)中进一步了解 `migrate` 命令。

## 变更摘要

下面是 Tauri 1.0 到 Tauri 2.0 的变更摘要：

### Tauri 配置

- `package > productName` 和 `package > version` 移到顶层对象。
- 二进制文件名不再自动重命名为与 `productName` 一致，因此你必须在顶层对象中添加与 `productName` 匹配的 `mainBinaryName` 字符串。
- `package` 已移除。
- `tauri` 键重命名为 `app`。
- `tauri > allowlist` 已移除。请参阅[迁移权限](#迁移权限)。
- `tauri > allowlist > protocol > assetScope` 移到 `app > security > assetProtocol > scope`。关于 `enable`、glob 模式、`requireLiteralLeadingDot` 和动态路径，请参阅[资源协议作用域](../../../security/5-assetprotocol/)。
- `tauri > cli` 移到 `plugins > cli`。
- `tauri > windows > fileDropEnabled` 重命名为 `app > windows > dragDropEnabled`。
- `tauri > updater > active` 已移除。
- `tauri > updater > dialog` 已移除。
- `tauri > updater` 移到 `plugins > updater`。
- 新增 `bundle > createUpdaterArtifacts`，使用应用更新器时必须设置。
  - 从已经分发的 v1 应用升级时，请将其设为 `v1Compatible`。更多信息请参阅[更新器指南](../../../plugin/28-updater/)。
- `tauri > systemTray` 重命名为 `app > trayIcon`。
- `tauri > pattern` 移到 `app > security > pattern`。
- `tauri > bundle` 移到顶层。
- `tauri > bundle > identifier` 移到顶层对象。
- `tauri > bundle > dmg` 移到 `bundle > macOS > dmg`
- `tauri > bundle > deb` 移到 `bundle > linux > deb`
- `tauri > bundle > appimage` 移到 `bundle > linux > appimage`
- `tauri > bundle > macOS > license` 已移除，请改用 `bundle > licenseFile`。
- `tauri > bundle > windows > wix > license` 已移除，请改用 `bundle > licenseFile`。
- `tauri > bundle > windows > nsis > license` 已移除，请改用 `bundle > licenseFile`。
- `tauri > bundle > windows > webviewFixedRuntimePath` 已移除，请改用 `bundle > windows > webviewInstallMode`。
- `build > withGlobalTauri` 移到 `app > withGlobalTauri`。
- `build > distDir` 重命名为 `frontendDist`。
- `build > devPath` 重命名为 `devUrl`。

[Tauri 2.0 配置 API 参考](https://tauri.app/reference/config/)

### 新增的 Cargo 特性

- linux-protocol-body：启用自定义协议请求体解析，允许 IPC 使用它。需要 webkit2gtk 2.40。

### 移除的 Cargo 特性

- reqwest-client：现在 reqwest 是唯一受支持的客户端。
- reqwest-native-tls-vendored：请改用 `native-tls-vendored`。
- process-command-api：请改用 `shell` 插件（说明见下一节）。
- shell-open-api：请改用 `shell` 插件（说明见下一节）。
- windows7-compat：移到 `notification` 插件。
- updater：更新器现在是一个插件。
- linux-protocol-headers：由于我们提升了最低 webkit2gtk 版本，现在默认启用。
- system-tray：重命名为 `tray-icon`。

### Rust crate 变更

- `api` 模块已移除。每个 API 模块都可以在对应的 Tauri 插件中找到。
- `api::dialog` 模块已移除。请改用 `tauri-plugin-dialog`。[迁移](#迁移到对话框插件)
- `api::file` 模块已移除。请改用 Rust 的 [`std::fs`](https://doc.rust-lang.org/std/fs/)。
- `api::http` 模块已移除。请改用 `tauri-plugin-http`。[迁移](#迁移到-http-插件)
- `api::ip` 模块已重写并移到 `tauri::ipc`。请查看新的 API，尤其是 `tauri::ipc::Channel`。
- `api::path` 模块的函数和 `tauri::PathResolved` 移到 `tauri::Manager::path`。[迁移](#将路径-api-迁移到-tauri-manager)
- `api::process::Command`、`tauri::api::shell` 和 `tauri::Manager::shell_scope` API 已移除。请改用 `tauri-plugin-shell`。[迁移](#迁移到-shell-插件)
- `api::process::current_binary` 和 `tauri::api::process::restart` 移到 `tauri::process`。
- `api::version` 模块已移除。请改用 [semver crate](https://docs.rs/semver/latest/semver/)。
- `App::clipboard_manager` 和 `AppHandle::clipboard_manager` 已移除。请改用 `tauri-plugin-clipboard`。[迁移](#迁移到剪贴板插件)
- `App::get_cli_matches` 已移除。请改用 `tauri-plugin-cli`。[迁移](#迁移到-cli-插件)
- `App::global_shortcut_manager` 和 `AppHandle::global_shortcut_manager` 已移除。请改用 `tauri-plugin-global-shortcut`。[迁移](#迁移到全局快捷键插件)
- `Manager::fs_scope` 已移除。文件系统作用域可以通过 `tauri_plugin_fs::FsExt` 访问。
- `Plugin::PluginApi` 现在接收插件配置作为第二个参数。
- `Plugin::setup_with_config` 已移除。请改用更新后的 `tauri::Plugin::PluginApi`。
- `scope::ipc::RemoteDomainAccessScope::enable_tauri_api` 和 `scope::ipc::RemoteDomainAccessScope::enables_tauri_api` 已移除。请改为通过 `scope::ipc::RemoteDomainAccessScope::add_plugin` 逐个启用核心插件。
- `scope::IpcScope` 已移除，请改用 `scope::ipc::Scope`。
- `scope::FsScope`、`scope::GlobPattern` 和 `scope::FsScopeEvent` 已移除，请分别改用 `scope::fs::Scope`、`scope::fs::Pattern` 和 `scope::fs::Event`。
- `updater` 模块已移除。请改用 `tauri-plugin-updater`。[迁移](#迁移到更新器插件)
- `Env.args` 字段已移除，请改用 `Env.args_os` 字段。
- `Menu`、`MenuEvent`、`CustomMenuItem`、`Submenu`、`WindowMenuEvent`、`MenuItem` 和 `Builder::on_menu_event` API 已移除。[迁移](#迁移到菜单模块)
- `SystemTray`、`SystemTrayHandle`、`SystemTrayMenu`、`SystemTrayMenuItemHandle`、`SystemTraySubmenu`、`MenuEntry` 和 `SystemTrayMenuItem` API 已移除。[迁移](#迁移到托盘图标模块)

### JavaScript API 变更

`@tauri-apps/api` 包不再提供非核心模块。现在只导出以前的 `tauri`（现为 `core`）、`path`、`event` 和 `window` 模块，其它模块都已移到插件中。

- `@tauri-apps/api/tauri` 模块重命名为 `@tauri-apps/api/core`。[迁移](#迁移到-core-模块)
- `@tauri-apps/api/cli` 模块已移除。请改用 `@tauri-apps/plugin-cli`。[迁移](#迁移到-cli-插件)
- `@tauri-apps/api/clipboard` 模块已移除。请改用 `@tauri-apps/plugin-clipboard`。[迁移](#迁移到剪贴板插件)
- `@tauri-apps/api/dialog` 模块已移除。请改用 `@tauri-apps/plugin-dialog`。[迁移](#迁移到对话框插件)
- `@tauri-apps/api/fs` 模块已移除。请改用 `@tauri-apps/plugin-fs`。[迁移](#迁移到文件系统插件)
- `@tauri-apps/api/global-shortcut` 模块已移除。请改用 `@tauri-apps/plugin-global-shortcut`。[迁移](#迁移到全局快捷键插件)
- `@tauri-apps/api/http` 模块已移除。请改用 `@tauri-apps/plugin-http`。[迁移](#迁移到-http-插件)
- `@tauri-apps/api/os` 模块已移除。请改用 `@tauri-apps/plugin-os`。[迁移](#迁移到-os-插件)
- `@tauri-apps/api/notification` 模块已移除。请改用 `@tauri-apps/plugin-notification`。[迁移](#迁移到通知插件)
- `@tauri-apps/api/process` 模块已移除。请改用 `@tauri-apps/plugin-process`。[迁移](#迁移到进程插件)
- `@tauri-apps/api/shell` 模块已移除。请改用 `@tauri-apps/plugin-shell`。[迁移](#迁移到-shell-插件)
- `@tauri-apps/api/updater` 模块已移除。请改用 `@tauri-apps/plugin-updater` [迁移](#迁移到更新器插件)
- `@tauri-apps/api/window` 模块重命名为 `@tauri-apps/api/webviewWindow`。[迁移](#迁移到新的窗口-api)

v1 插件现在以 `@tauri-apps/plugin-<plugin-name>` 的形式发布。以前它们以 `tauri-plugin-<plugin-name>-api` 的形式从 git 获取。

### 环境变量变更

Tauri CLI 读写的大部分环境变量都已重命名，以保持一致并避免出错：

- `TAURI_PRIVATE_KEY` -> `TAURI_SIGNING_PRIVATE_KEY`
- `TAURI_KEY_PASSWORD` -> `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`
- `TAURI_SKIP_DEVSERVER_CHECK` -> `TAURI_CLI_NO_DEV_SERVER_WAIT`
- `TAURI_DEV_SERVER_PORT` -> `TAURI_CLI_PORT`
- `TAURI_PATH_DEPTH` -> `TAURI_CLI_CONFIG_DEPTH`
- `TAURI_FIPS_COMPLIANT` -> `TAURI_BUNDLER_WIX_FIPS_COMPLIANT`
- `TAURI_DEV_WATCHER_IGNORE_FILE` -> `TAURI_CLI_WATCHER_IGNORE_FILENAME`
- `TAURI_TRAY` -> `TAURI_LINUX_AYATANA_APPINDICATOR`
- `TAURI_APPLE_DEVELOPMENT_TEAM` -> `APPLE_DEVELOPMENT_TEAM`
- `TAURI_PLATFORM` -> `TAURI_ENV_PLATFORM`
- `TAURI_ARCH` -> `TAURI_ENV_ARCH`
- `TAURI_FAMILY` -> `TAURI_ENV_FAMILY`
- `TAURI_PLATFORM_VERSION` -> `TAURI_ENV_PLATFORM_VERSION`
- `TAURI_PLATFORM_TYPE` -> `TAURI_ENV_PLATFORM_TYPE`
- `TAURI_DEBUG` -> `TAURI_ENV_DEBUG`

### 事件系统

事件系统经过重新设计，更易于使用。它不再依赖事件来源，而是采用了基于事件目标的更简单实现。

- `emit` 函数现在会把事件发送给所有事件监听器。
- 新增 `emit_to`/`emitTo` 函数，用于向特定目标触发事件。
- `emit_filter` 现在基于 [`EventTarget`](https://docs.rs/tauri/2.0.0/tauri/event/enum.EventTarget.html) 过滤，而不是基于窗口。
- `listen_global` 重命名为 `listen_any`。它现在会监听所有事件，无论其过滤器和目标是什么。
- JavaScript：`event.listen()` 的行为类似于 `listen_any`。除非在 `Options` 中设置了目标，否则它现在会监听所有事件，无论其过滤器和目标是什么。
- JavaScript：`WebviewWindow.listen` 等只监听发送给对应 `EventTarget` 的事件。

### 多 webview 支持

Tauri v2 引入了多 webview 支持，目前位于 `unstable` 特性标志之后。
为了支持它，我们把 Rust 的 `Window` 类型重命名为 `WebviewWindow`，把 Manager 的 `get_window` 函数重命名为 `get_webview_window`。

`WebviewWindow` 的 JS API 类型现在从 `@tauri-apps/api/webviewWindow` 重新导出，而不是 `@tauri-apps/api/window`。

### Windows 上新的源 URL

在 Windows 上，生产应用的前端文件现在托管在 `http://tauri.localhost`，而不是 `https://tauri.localhost`。因此，除非在 v1 中使用过 `dangerousUseHttpScheme`，IndexedDB、LocalStorage 和 Cookies 都会被重置。要避免这一点，你可以把 `app > windows > useHttpsScheme` 设为 `true`，或使用 `WebviewWindowBuilder::use_https_scheme` 继续使用 `https` 方案。

## 详细迁移步骤

将 Tauri 1.0 应用迁移到 Tauri 2.0 时可能遇到的常见场景。

### 迁移到 Core 模块

`@tauri-apps/api/tauri` 模块已重命名为 `@tauri-apps/api/core`。
只需重命名模块导入：

```diff
- import { invoke } from "@tauri-apps/api/tauri"
+ import { invoke } from "@tauri-apps/api/core"
```

### 迁移到 CLI 插件

Rust 的 `App::get_cli_matches` 和 JavaScript 的 `@tauri-apps/api/cli` API 已移除。请改用 `@tauri-apps/plugin-cli` 插件：

1. 添加到 cargo 依赖：

```toml
[dependencies]
tauri-plugin-cli = "2"
```

2. 在 JavaScript 或 Rust 项目中使用：

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```rust
fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_cli::init())
}
```

```json
{
  "dependencies": {
    "@tauri-apps/plugin-cli": "^2.0.0"
  }
}
```

```javascript
import { getMatches } from '@tauri-apps/plugin-cli';
const matches = await getMatches();
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
fn main() {
    use tauri_plugin_cli::CliExt;
    tauri::Builder::default()
        .plugin(tauri_plugin_cli::init())
        .setup(|app| {
            let cli_matches = app.cli().matches()?;
            Ok(())
        })
}
```

{{% /tab %}}

{{< /tabpane >}}
### 迁移到剪贴板插件

Rust 的 `App::clipboard_manager` 和 `AppHandle::clipboard_manager`，以及 JavaScript 的 `@tauri-apps/api/clipboard` API 已移除。请改用 `@tauri-apps/plugin-clipboard-manager` 插件：

```toml
tauri-plugin-clipboard-manager = "2"
```

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```rust
fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_clipboard_manager::init())
}
```

```json
{
  "dependencies": {
    "@tauri-apps/plugin-clipboard-manager": "^2.0.0"
  }
}
```

```javascript
import { writeText, readText } from '@tauri-apps/plugin-clipboard-manager';
await writeText('Tauri is awesome!');
assert(await readText(), 'Tauri is awesome!');
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
use tauri_plugin_clipboard::{ClipboardExt, ClipKind};
tauri::Builder::default()
    .plugin(tauri_plugin_clipboard::init())
    .setup(|app| {
        app.clipboard().write(ClipKind::PlainText {
            label: None,
            text: "Tauri is awesome!".into(),
        })?;
        Ok(())
    })
```

{{% /tab %}}

{{< /tabpane >}}
### 迁移到对话框插件

Rust 的 `tauri::api::dialog` 和 JavaScript 的 `@tauri-apps/api/dialog` API 已移除。请改用 `@tauri-apps/plugin-dialog` 插件：

1. 添加到 cargo 依赖：

```toml
[dependencies]
tauri-plugin-dialog = "2"
```

2. 在 JavaScript 或 Rust 项目中使用：

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```rust
fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
}
```

```json
{
  "dependencies": {
    "@tauri-apps/plugin-dialog": "^2.0.0"
  }
}
```

```javascript
import { save } from '@tauri-apps/plugin-dialog';
const filePath = await save({
  filters: [
    {
      name: 'Image',
      extensions: ['png', 'jpeg'],
    },
  ],
});
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
tauri::Builder::default()
    .plugin(tauri_plugin_dialog::init())
    .setup(|app| {
        app.dialog().file().pick_file(|file_path| {
            // 在这里处理可选的文件路径
            // 如果用户关闭了对话框，文件路径为 `None`
        });

        app.dialog().message("Tauri is Awesome!").show();
        Ok(())
     })
```

{{% /tab %}}

{{< /tabpane >}}
### 迁移到文件系统插件

Rust 的 `tauri::api::file` 和 JavaScript 的 `@tauri-apps/api/fs` API 已移除。Rust 请改用 [`std::fs`](https://doc.rust-lang.org/std/fs/)，JavaScript 请改用 `@tauri-apps/plugin-fs` 插件：

1. 添加到 cargo 依赖：

```toml
[dependencies]
tauri-plugin-fs = "2"
```

2. 在 JavaScript 或 Rust 项目中使用：

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```rust
fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_fs::init())
}
```

```json
{
  "dependencies": {
    "@tauri-apps/plugin-fs": "^2.0.0"
  }
}
```

```javascript
import { mkdir, BaseDirectory } from '@tauri-apps/plugin-fs';
await mkdir('db', { baseDir: BaseDirectory.AppLocalData });
```

一些函数和类型已被重命名或移除：

- `Dir` 枚举别名已移除，请使用 `BaseDirectory`。
- `FileEntry`、`FsBinaryFileOption`、`FsDirOptions`、`FsOptions`、`FsTextFileOption` 和 `BinaryFileContents` 等接口与类型别名已移除，替换为适合各函数的新接口。
- `createDir` 重命名为 `mkdir`。
- `readBinaryFile` 重命名为 `readFile`。
- `removeDir` 已移除，改用 `remove`。
- `removeFile` 已移除，改用 `remove`。
- `renameFile` 已移除，改用 `rename`。
- `writeBinaryFile` 重命名为 `writeFile`。

{{% /tab %}}

{{% tab header="Rust" %}}

使用 Rust 的 [`std::fs`](https://doc.rust-lang.org/std/fs/) 函数。

{{% /tab %}}

{{< /tabpane >}}
### 迁移到全局快捷键插件

Rust 的 `App::global_shortcut_manager` 和 `AppHandle::global_shortcut_manager`，以及 JavaScript 的 `@tauri-apps/api/global-shortcut` API 已移除。请改用 `@tauri-apps/plugin-global-shortcut` 插件：

1. 添加到 cargo 依赖：

```toml
[dependencies]
[target."cfg(not(any(target_os = \"android\", target_os = \"ios\")))".dependencies]
tauri-plugin-global-shortcut = "2"
```

2. 在 JavaScript 或 Rust 项目中使用：

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```rust
fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_global_shortcut::Builder::default().build())
}
```

```json
{
  "dependencies": {
    "@tauri-apps/plugin-global-shortcut": "^2.0.0"
  }
}
```

```javascript
import { register } from '@tauri-apps/plugin-global-shortcut';
await register('CommandOrControl+Shift+C', () => {
  console.log('Shortcut triggered');
});
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust

tauri::Builder::default()
    .plugin(
        tauri_plugin_global_shortcut::Builder::new().with_handler(|app, shortcut| {
            println!("Shortcut triggered: {:?}", shortcut);
        })
        .build(),
    )
    .setup(|app| {
        // 注册一个全局快捷键
        // 在 macOS 上使用 Cmd 键
        // 在 Windows 和 Linux 上使用 Ctrl 键
        app.global_shortcut().register("CmdOrCtrl+Y")?;
        Ok(())
    })
```

{{% /tab %}}

{{< /tabpane >}}
### 迁移到 HTTP 插件

Rust 的 `tauri::api::http` 和 JavaScript 的 `@tauri-apps/api/http` API 已移除。请改用 `@tauri-apps/plugin-http` 插件：

1. 添加到 cargo 依赖：

```toml
[dependencies]
tauri-plugin-http = "2"
```

2. 在 JavaScript 或 Rust 项目中使用：

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```rust
fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_http::init())
}
```

```json
{
  "dependencies": {
    "@tauri-apps/plugin-http": "^2.0.0"
  }
}
```

```javascript
import { fetch } from '@tauri-apps/plugin-http';
const response = await fetch(
  'https://raw.githubusercontent.com/tauri-apps/tauri/dev/package.json'
);
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust

tauri::Builder::default()
    .plugin(tauri_plugin_http::init())
    .setup(|app| {
        let response_data = tauri::async_runtime::block_on(async {
            let response = reqwest::get(
                "https://raw.githubusercontent.com/tauri-apps/tauri/dev/package.json",
            )
            .await
            .unwrap();
            response.text().await
        })?;
        Ok(())
    })
```

HTTP 插件重新导出了 [reqwest](https://docs.rs/reqwest/latest/reqwest/)，你可以查阅它的文档了解更多信息。

{{% /tab %}}

{{< /tabpane >}}
### 迁移到通知插件

Rust 的 `tauri::api::notification` 和 JavaScript 的 `@tauri-apps/api/notification` API 已移除。请改用 `@tauri-apps/plugin-notification` 插件：

1. 添加到 cargo 依赖：

```toml
[dependencies]
tauri-plugin-notification = "2"
```

2. 在 JavaScript 或 Rust 项目中使用：

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```rust
fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_notification::init())
}
```

```json
{
  "dependencies": {
    "@tauri-apps/plugin-notification": "^2.0.0"
  }
}
```

```javascript
import { sendNotification } from '@tauri-apps/plugin-notification';
sendNotification('Tauri is awesome!');
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
use tauri::plugin::PermissionState;

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_notification::init())
        .setup(|app| {
            if app.notification().permission_state()? == PermissionState::Unknown {
                app.notification().request_permission()?;
            }
            if app.notification().permission_state()? == PermissionState::Granted {
                app.notification()
                    .builder()
                    .body("Tauri is awesome!")
                    .show()?;
            }
            Ok(())
        })
}
```

{{% /tab %}}

{{< /tabpane >}}
### 迁移到菜单模块

Rust 的 `Menu` API 已移到 `tauri::menu` 模块，并重构为使用 [muda crate](https://github.com/tauri-apps/muda)。

#### 使用 `tauri::menu::MenuBuilder`

请使用 `tauri::menu::MenuBuilder` 替代 `tauri::Menu`。注意它的构造函数接收一个 Manager 实例（`App`、`AppHandle` 或 `WebviewWindow` 之一）作为参数：

```rust

tauri::Builder::default()
    .setup(|app| {
        let menu = MenuBuilder::new(app)
            .copy()
            .paste()
            .separator()
            .undo()
            .redo()
            .text("open-url", "Open URL")
            .check("toggle", "Toggle")
            .icon("show-app", "Show App", app.default_window_icon().cloned().unwrap())
            .build()?;
        app.set_menu(menu);
        Ok(())
    })
```

#### 使用 `tauri::menu::PredefinedMenuItem`

请使用 `tauri::menu::PredefinedMenuItem` 替代 `tauri::MenuItem`：

```rust
use tauri::menu::{MenuBuilder, PredefinedMenuItem};

tauri::Builder::default()
    .setup(|app| {
        let menu = MenuBuilder::new(app).item(&PredefinedMenuItem::copy(app)?).build()?;
        Ok(())
    })
```

{{% alert title="提示" %}}
菜单构建器为每个预定义菜单项都提供了专用方法，因此你可以调用 `.copy()`，而不必写 `.item(&PredefinedMenuItem::copy(app, None)?)`。
{{% /alert %}}

#### 使用 `tauri::menu::MenuItemBuilder`

请使用 `tauri::menu::MenuItemBuilder` 替代 `tauri::CustomMenuItem`：

```rust

tauri::Builder::default()
    .setup(|app| {
        let toggle = MenuItemBuilder::new("Toggle").accelerator("Ctrl+Shift+T").build(app)?;
        Ok(())
    })
```

#### 使用 `tauri::menu::SubmenuBuilder`

请使用 `tauri::menu::SubmenuBuilder` 替代 `tauri::Submenu`：

```rust
use tauri::menu::{MenuBuilder, SubmenuBuilder};

tauri::Builder::default()
    .setup(|app| {
        let submenu = SubmenuBuilder::new(app, "Sub")
            .text("Tauri")
            .separator()
            .check("Is Awesome")
            .build()?;
        let menu = MenuBuilder::new(app).item(&submenu).build()?;
        Ok(())
    })
```

`tauri::Builder::menu` 现在接收一个闭包，因为构建菜单需要一个 Manager 实例。更多信息请参阅[文档](https://docs.rs/tauri/2.0.0/tauri/struct.Builder.html#method.menu)。

#### 菜单事件

Rust 的 `tauri::Builder::on_menu_event` API 已移除。请改用 `tauri::App::on_menu_event` 或 `tauri::AppHandle::on_menu_event`：

```rust
use tauri::menu::{CheckMenuItemBuilder, MenuBuilder, MenuItemBuilder};

tauri::Builder::default()
    .setup(|app| {
        let toggle = MenuItemBuilder::with_id("toggle", "Toggle").build(app)?;
        let check = CheckMenuItemBuilder::new("Mark").build(app)?;
        let menu = MenuBuilder::new(app).items(&[&toggle, &check]).build()?;

        app.set_menu(menu)?;

        app.on_menu_event(move |app, event| {
            if event.id() == check.id() {
                println!("`check` triggered, do something! is checked? {}", check.is_checked().unwrap());
            } else if event.id() == "toggle" {
                println!("toggle triggered!");
            }
        });
        Ok(())
    })
```

注意，有两种方式判断选中的是哪个菜单项：把菜单项移动到事件处理闭包中并比较 ID，或者通过 `with_id` 构造函数为该菜单项定义自定义 ID，再用该 ID 字符串进行比较。

{{% alert title="提示" %}}
菜单项可以在多个菜单之间共享，而菜单事件绑定到菜单项上，而不是绑定到菜单或窗口上。
如果你不希望选中某个菜单项时触发所有监听器，就不要共享菜单项，而应为每个菜单使用独立实例，并把它们移入 `tauri::WebviewWindow/WebviewWindowBuilder::on_menu_event` 闭包中。
{{% /alert %}}

### 迁移到 OS 插件

Rust 的 `tauri::api::os` 和 JavaScript 的 `@tauri-apps/api/os` API 已移除。请改用 `@tauri-apps/plugin-os` 插件：

1. 添加到 cargo 依赖：

```toml
[dependencies]
tauri-plugin-os = "2"
```

2. 在 JavaScript 或 Rust 项目中使用：

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```rust
fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_os::init())
}
```

```json
{
  "dependencies": {
    "@tauri-apps/plugin-os": "^2.0.0"
  }
}
```

```javascript
import { arch } from '@tauri-apps/plugin-os';
const architecture = await arch();
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_os::init())
        .setup(|app| {
            let os_arch = tauri_plugin_os::arch();
            Ok(())
        })
}
```

{{% /tab %}}

{{< /tabpane >}}
### 迁移到进程插件

Rust 的 `tauri::api::process` 和 JavaScript 的 `@tauri-apps/api/process` API 已移除。请改用 `@tauri-apps/plugin-process` 插件：

1. 添加到 cargo 依赖：

```toml
[dependencies]
tauri-plugin-process = "2"
```

2. 在 JavaScript 或 Rust 项目中使用：

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```rust
fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_process::init())
}
```

```json
{
  "dependencies": {
    "@tauri-apps/plugin-process": "^2.0.0"
  }
}
```

```javascript
import { exit, relaunch } from '@tauri-apps/plugin-process';
await exit(0);
await relaunch();
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_process::init())
        .setup(|app| {
            // 以某个状态码退出应用
            app.handle().exit(1);
            // 重启应用
            app.handle().restart();
            Ok(())
        })
}
```

{{% /tab %}}

{{< /tabpane >}}
### 迁移到 Shell 插件

Rust 的 `tauri::api::shell` 和 JavaScript 的 `@tauri-apps/api/shell` API 已移除。请改用 `@tauri-apps/plugin-shell` 插件：

1. 添加到 cargo 依赖：

```toml
[dependencies]
tauri-plugin-shell = "2"
```

2. 在 JavaScript 或 Rust 项目中使用：

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```rust
fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
}
```

```json
{
  "dependencies": {
    "@tauri-apps/plugin-shell": "^2.0.0"
  }
}
```

```javascript
import { Command, open } from '@tauri-apps/plugin-shell';
const output = await Command.create('echo', 'message').execute();

await open('https://github.com/tauri-apps/tauri');
```

{{% /tab %}}

{{% tab header="Rust" %}}

- 打开一个 URL

```rust

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            app.shell().open("https://github.com/tauri-apps/tauri", None)?;
            Ok(())
        })
}
```

- 启动子进程并获取状态码

```rust

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            let status = tauri::async_runtime::block_on(async move { app.shell().command("which").args(["ls"]).status().await.unwrap() });
            println!("`which` finished with status: {:?}", status.code());
            Ok(())
        })
}
```

- 启动子进程并捕获其输出

```rust

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            let output = tauri::async_runtime::block_on(async move { app.shell().command("echo").args(["TAURI"]).output().await.unwrap() });
            assert!(output.status.success());
            assert_eq!(String::from_utf8(output.stdout).unwrap(), "TAURI");
            Ok(())
        })
}
```

- 启动子进程并异步读取其事件：

```rust
use tauri_plugin_shell::{ShellExt, process::CommandEvent};

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            let handle = app.handle().clone();
            tauri::async_runtime::spawn(async move {
                let (mut rx, mut child) = handle.shell().command("cargo")
                    .args(["tauri", "dev"])
                    .spawn()
                    .expect("Failed to spawn cargo");

                let mut i = 0;
                while let Some(event) = rx.recv().await {
                    if let CommandEvent::Stdout(line) = event {
                        println!("got: {}", String::from_utf8(line).unwrap());
                       i += 1;
                       if i == 4 {
                           child.write("message from Rust\n".as_bytes()).unwrap();
                           i = 0;
                       }
                   }
                }
            });
            Ok(())
        })
}
```

{{% /tab %}}

{{< /tabpane >}}
### 迁移到托盘图标模块

为保持一致，Rust 的 `SystemTray` API 已重命名为 `TrayIcon`。新的 API 位于 Rust 的 `tray` 模块中。

#### 使用 `tauri::tray::TrayIconBuilder`

请使用 `tauri::tray::TrayIconBuilder` 替代 `tauri::SystemTray`：

```rust
let tray = tauri::tray::TrayIconBuilder::with_id("my-tray").build(app)?;
```

更多信息请参阅 [TrayIconBuilder](https://docs.rs/tauri/2.0.0/tauri/tray/struct.TrayIconBuilder.html)。

#### 迁移到 Menu

请使用 `tauri::menu::Menu` 替代 `tauri::SystemTrayMenu`，使用 `tauri::menu::Submenu` 替代 `tauri::SystemTraySubmenu`，使用 `tauri::menu::PredefinedMenuItem` 替代 `tauri::SystemTrayMenuItem`。

#### 托盘事件

`tauri::SystemTray::on_event` 已拆分为 `tauri::tray::TrayIconBuilder::on_menu_event` 和 `tauri::tray::TrayIconBuilder::on_tray_icon_event`：

```rust
use tauri::{
    menu::{MenuBuilder, MenuItemBuilder},
    tray::{MouseButton, MouseButtonState, TrayIconBuilder, TrayIconEvent},
};

tauri::Builder::default()
    .setup(|app| {
        let toggle = MenuItemBuilder::with_id("toggle", "Toggle").build(app)?;
        let menu = MenuBuilder::new(app).items(&[&toggle]).build()?;
        let tray = TrayIconBuilder::new()
            .menu(&menu)
            .on_menu_event(move |app, event| match event.id().as_ref() {
                "toggle" => {
                    println!("toggle clicked");
                }
                _ => (),
            })
            .on_tray_icon_event(|tray, event| {
                if let TrayIconEvent::Click {
                        button: MouseButton::Left,
                        button_state: MouseButtonState::Up,
                        ..
                } = event
                {
                    let app = tray.app_handle();
                    if let Some(webview_window) = app.get_webview_window("main") {
                       let _ = webview_window.unminimize();
                       let _ = webview_window.show();
                       let _ = webview_window.set_focus();
                    }
                }
            })
            .build(app)?;

        Ok(())
    })
```

### 迁移到更新器插件

{{% alert title="默认行为变更" color="warning" %}}

带有自动更新检查的内置对话框已移除，请改用 Rust 和 JS API 来检查和安装更新。否则你的用户将无法继续获取更新！

{{% /alert %}}

Rust 的 `tauri::updater` 和 JavaScript 的 `@tauri-apps/api-updater` API 已移除。要使用 `@tauri-apps/plugin-updater` 设置自定义更新目标：

1. 添加到 cargo 依赖：

```toml
tauri-plugin-updater = "2"
```

2. 在 JavaScript 或 Rust 项目中使用：

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

```rust
fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_updater::Builder::new().build())
}
```

```json
{
  "dependencies": {
    "@tauri-apps/plugin-updater": "^2.0.0"
  }
}
```

```javascript
import { check } from '@tauri-apps/plugin-updater';
import { relaunch } from '@tauri-apps/plugin-process';

const update = await check();
if (update?.available) {
  console.log(`Update to ${update.version} available! Date: ${update.date}`);
  console.log(`Release notes: ${update.body}`);
  await update.downloadAndInstall();
  // 需要 `process` 插件
  await relaunch();
}
```

{{% /tab %}}

{{% tab header="Rust" %}}

检查更新：

```rust

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_updater::Builder::new().build())
        .setup(|app| {
            let handle = app.handle();
            tauri::async_runtime::spawn(async move {
                let response = handle.updater().check().await;
            });
            Ok(())
        })
}
```

设置自定义更新目标：

```rust
fn main() {
    let mut updater = tauri_plugin_updater::Builder::new();
    #[cfg(target_os = "macos")]
    {
        updater = updater.target("darwin-universal");
    }
    tauri::Builder::default()
        .plugin(updater.build())
}
```

{{% /tab %}}

{{< /tabpane >}}
### 将路径 API 迁移到 Tauri Manager

Rust 的 `tauri::api::path` 模块函数和 `tauri::PathResolver` 已移到 `tauri::Manager::path`：

```rust
use tauri::{path::BaseDirectory, Manager};

tauri::Builder::default()
    .setup(|app| {
        let home_dir_path = app.path().home_dir().expect("failed to get home dir");

        let path = app.path().resolve("path/to/something", BaseDirectory::Config)?;

        Ok(())
  })
```

### 迁移到新的窗口 API

在 Rust 侧，`Window` 已重命名为 `WebviewWindow`，其构建器 `WindowBuilder` 现在名为 `WebviewWindowBuilder`，`WindowUrl` 现在名为 `WebviewUrl`。

此外，`Manager::get_window` 函数已重命名为 `get_webview_window`，窗口的 `parent_window` API 已重命名为 `parent_raw`，以支持更高层的窗口父级 API。

在 JavaScript 侧，`WebviewWindow` 类现在从 `@tauri-apps/api/webviewWindow` 路径导出。

`onMenuClicked` 函数已移除，你可以改为在 JavaScript 中创建菜单时拦截菜单事件。

### 迁移嵌入的附加文件（资源）

在 JavaScript 侧，请确保完成[迁移到文件系统插件](#迁移到文件系统插件)。
此外，请注意 v1 allowlist 在[迁移权限](#迁移权限)中所做的变更。

在 Rust 侧，请确保完成[将路径 API 迁移到 Tauri Manager](#将路径-api-迁移到-tauri-manager)。

### 迁移嵌入的外部二进制文件（Sidecar）

在 Tauri v1 中，外部二进制文件及其参数在 allowlist 中定义。在 v2 中，请使用新的权限系统。更多信息请阅读[迁移权限](#迁移权限)。

在 JavaScript 侧，请确保完成[迁移到 Shell 插件](#迁移到-shell-插件)。

在 Rust 侧，`tauri::api::process` API 已移除。请改用 `tauri_plugin_shell::ShellExt` 和 `tauri_plugin_shell::process::CommandEvent` API。如何操作请阅读[嵌入外部二进制文件](../../../develop/7-sidecar/#从-rust-运行)指南。

“process-command-api” 特性标志在 v2 中已移除。因此运行外部二进制文件不再需要在 Tauri 配置中定义该特性。

### 迁移权限

v1 的 allowlist 已被完全重写为全新的权限系统，它适用于各个插件，并且在多窗口和远程 URL 支持方面可配置性强得多。
这个新系统的工作方式类似访问控制列表（ACL）：你可以允许或拒绝命令、把权限分配给特定的窗口和域集合，并定义访问作用域。

要为你的应用启用权限，你必须在 `src-tauri/capabilities` 文件夹中创建能力文件，Tauri 会自动为你配置其它所有内容。

`migrate` CLI 命令会自动解析你的 v1 allowlist 并生成相关的能力文件。

要进一步了解权限和能力，请参阅[安全文档](../../../security/1-overview/)。
