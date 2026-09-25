+++
title = "1 插件开发"
date = 2026-09-25T21:31:08+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/plugins/](https://tauri.app/develop/plugins/)

{{% alert title="插件开发" %}}

本指南面向 Tauri 插件的开发。如果你想要的是当前可用插件列表以及如何使用它们，请访问[功能与示例列表](../../../plugin/1-overview/)。

{{% /alert %}}

插件可以挂接到 Tauri 的生命周期、暴露依赖 web view API 的 Rust 代码、用 Rust、Kotlin 或 Swift 代码处理命令，等等。

Tauri 提供了带 web view 功能的窗口系统、在 Rust 进程与 web view 之间发送消息的方式，以及事件系统和若干提升开发体验的工具。按照设计，Tauri 核心不包含并非所有人都需要的功能，而是提供了一种把外部功能加入 Tauri 应用的机制，也就是插件。

一个 Tauri 插件由一个 Cargo crate 和一个可选的 NPM 包组成，后者为其命令和事件提供 API 绑定。此外，插件项目还可以包含一个 Android 库项目和一个用于 iOS 的 Swift 包。你可以在[移动端插件开发指南](../2-developmobile/)中进一步了解如何为 Android 和 iOS 开发插件。

## 命名约定

Tauri 插件有一个前缀，后面跟着插件名。插件名在插件配置中的 [`tauri.conf.json > plugins`](https://tauri.app/reference/config/#pluginconfig) 下指定。

默认情况下，Tauri 会给你的插件 crate 加上 `tauri-plugin-` 前缀。这有助于你的插件被 Tauri 社区发现，并能与 Tauri CLI 一起使用。初始化新插件项目时，你必须提供它的名称。生成的 crate 名将是 `tauri-plugin-{plugin-name}`，JavaScript NPM 包名将是 `tauri-plugin-{plugin-name}-api`（不过我们建议尽可能使用 [NPM scope](https://docs.npmjs.com/about-scopes)）。Tauri 对 NPM 包的命名约定是 `@scope-name/plugin-{plugin-name}`。

### 标识符规则

插件 crate 中的 `{plugin-name}` 部分，以及能力（capabilities）中引用的任何权限标识符，都必须遵循 Tauri 的标识符语法：

- 小写 ASCII 字母（`a` 到 `z`）、数字（`0` 到 `9`）和连字符（`-`）。
- 连字符不能出现在首字符或末字符。
- 只有当标识符使用了前缀时（例如 `<plugin-name>:<permission-name>`），才允许出现单个冒号（`:`）。
- 不允许下划线（`_`）、大写字母以及其它字符。
- 基础名限制为 64 个字符；带前缀时，完整标识符限制为 129 个字符。

示例：

| 标识符                     |         是否有效？       |
| ------------------------- | :---------------------: |
| `sqlite`                  |            ✓            |
| `sqlite-store`            |            ✓            |
| `sqlite-store:allow-read` |            ✓            |
| `sqlite_store`            |     ✗（下划线）      |
| `SqliteStore`             |      ✗（大写）      |
| `-sqlite`                 |   ✗（前导连字符）    |
| `sqlite-`                 |   ✗（末尾连字符）   |
| `sqlite::store`           | ✗（多个分隔符） |

如果某个插件或权限标识符违反了这些规则，构建会失败并报错 `identifiers can only include lowercase ASCII, hyphens which are not leading or trailing, and a single colon if using a prefix`。违规值通常是你插件 `Cargo.toml` 中的插件名，或某个 `permissions/*.toml` 文件中的权限标识符。

## 初始化插件项目

要引导创建一个新的插件项目，请运行 `plugin new`。如果你不需要 NPM 包，请使用 `--no-api` CLI 标志。如果你想初始化带 Android 和／或 iOS 支持的插件，请使用 `--android` 和／或 `--ios` 标志。

安装之后，你可以运行以下命令创建一个插件项目：

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npx @tauri-apps/cli plugin new [name]
```

{{% /tab %}}

{{< /tabpane >}}
这会在 `tauri-plugin-[name]` 目录中初始化插件，根据所使用的 CLI 标志，生成的项目结构大致如下：

```
. tauri-plugin-[name]/
├── src/                - Rust 代码
│ ├── commands.rs       - 定义 webview 可以使用的命令
| ├── desktop.rs        - 桌面端实现
| ├── error.rs          - 返回结果中使用的默认错误类型
│ ├── lib.rs            - 重新导出合适的实现、设置 state 等
│ ├── mobile.rs         - 移动端实现
│ └── models.rs         - 共享结构体
├── permissions/        - 存放（生成的）命令权限文件
├── android             - Android 库
├── ios                 - Swift 包
├── guest-js            - JavaScript API 绑定的源代码
├── dist-js             - 由 guest-js 转译出的产物
├── Cargo.toml          - Cargo crate 元数据
└── package.json        - NPM 包元数据
```

如果你已有插件并想为它添加 Android 或 iOS 能力，可以使用 `plugin android add` 和 `plugin ios add` 来引导生成移动端库项目，并指导你完成所需的改动。

## 声明平台支持

插件可以在 crate 的 `Cargo.toml` 中的 `[package.metadata.platforms.support]` 一节声明自己支持哪些平台以及支持程度：

```toml
windows = { level = "full" }
linux = { level = "full" }
macos = { level = "full" }
android = { level = "partial", notes = "Access is restricted to the Application folder by default" }
ios = { level = "none" }
```

每个键是一个平台（`windows`、`linux`、`macos`、`android`、`ios`），接受两个字段：

- `level`（必填）：如果插件按预期工作则为 `"full"`，如果有功能限制则为 `"partial"`，如果不支持该平台则为 `"none"`。
- `notes`（可选）：对注意事项或限制的简短说明。它会以 Markdown 形式渲染在插件页面上。在[支持表](../../../plugin/1-overview/#支持表)中，它作为纯文本显示在工具提示里。

[功能与示例](../../../plugin/1-overview/)页面上的支持表和平台过滤器就是由这些元数据生成的。

## 移动端插件开发

插件可以运行用 Kotlin（或 Java）和 Swift 编写的原生移动端代码。默认插件模板包含一个使用 Kotlin 的 Android 库项目和一个 Swift 包。其中包含一个示例移动端命令，演示如何从 Rust 代码触发它的执行。

更多关于移动端插件开发的内容请阅读[移动端插件开发指南](../2-developmobile/)。

## 插件配置

在使用该插件的 Tauri 应用中，插件配置在 `tauri.conf.json` 中指定，其中 `plugin-name` 是插件名：

```json
{
  "build": { ... },
  "tauri": { ... },
  "plugins": {
    "plugin-name": {
      "timeout": 30
    }
  }
}
```

插件的配置设置在 `Builder` 上，并在运行时解析。下面是使用 `Config` 结构体指定插件配置的示例：

```rust
use tauri::{
    plugin::{Builder, TauriPlugin},
    Runtime,
};

// 定义插件配置
#[derive(Deserialize)]
pub struct Config {
  timeout: usize,
}

pub fn init<R: Runtime>() -> TauriPlugin<R, Config> {
  // 通过改用 `Builder::<R, Option<Config>>` 让插件配置变为可选
  Builder::<R, Config>::new("<plugin-name>")
    .setup(|app, api| {
      let timeout = api.config().timeout;
      Ok(())
    })
    .build()
}
```

## 生命周期事件

插件可以挂接到若干生命周期事件：

- [setup](#setup)：插件正在初始化
- [on_navigation](#on_navigation)：web view 正在尝试进行导航
- [on_webview_ready](#on_webview_ready)：新窗口正在创建
- [on_event](#on_event)：事件循环事件
- [on_drop](#on_drop)：插件正在被析构

移动端插件还有额外的[生命周期事件](../2-developmobile/#生命周期事件)。

### setup

- **时机**：插件正在初始化
- **用途**：注册移动端插件、管理 state、运行后台任务

```rust
use tauri::{Manager, plugin::Builder};
use std::{collections::HashMap, sync::Mutex, time::Duration};

struct DummyStore(Mutex<HashMap<String, String>>);

Builder::new("<plugin-name>")
  .setup(|app, api| {
    app.manage(DummyStore(Default::default()));

    let app_ = app.clone();
    std::thread::spawn(move || {
      loop {
        app_.emit("tick", ());
        std::thread::sleep(Duration::from_secs(1));
      }
    });

    Ok(())
  })
```

### on_navigation

- **时机**：web view 正在尝试进行导航
- **用途**：校验导航或跟踪 URL 变化

返回 `false` 会取消该导航。

```rust

Builder::new("<plugin-name>")
  .on_navigation(|window, url| {
    println!("window {} is navigating to {}", window.label(), url);
    // 如果被禁止则取消该导航
    url.scheme() != "forbidden"
  })
```

### on_webview_ready

- **时机**：新窗口已创建
- **用途**：为每个窗口执行初始化脚本

```rust

Builder::new("<plugin-name>")
  .on_webview_ready(|window| {
    window.listen("content-loaded", |event| {
      println!("webview content has been loaded");
    });
  })
```

### on_event

- **时机**：事件循环事件
- **用途**：处理窗口事件、菜单事件、应用退出请求等核心事件

通过这个生命周期钩子，你可以收到任何事件循环[事件](https://docs.rs/tauri/2.0.0/tauri/enum.RunEvent.html)的通知。

```rust
use std::{collections::HashMap, fs::write, sync::Mutex};
use tauri::{plugin::Builder, Manager, RunEvent};

struct DummyStore(Mutex<HashMap<String, String>>);

Builder::new("<plugin-name>")
  .setup(|app, _api| {
    app.manage(DummyStore(Default::default()));
    Ok(())
  })
  .on_event(|app, event| {
    match event {
      RunEvent::ExitRequested { api, .. } => {
        // 用户请求关闭某个窗口，并且已经没有窗口剩余

        // 我们可以阻止应用退出：
        api.prevent_exit();
      }
      RunEvent::Exit => {
        // 应用即将退出，你可以在这里做清理

        let store = app.state::<DummyStore>();
        write(
          app.path().app_local_data_dir().unwrap().join("store.json"),
          serde_json::to_string(&*store.0.lock().unwrap()).unwrap(),
        )
        .unwrap();
      }
      _ => {}
    }
  })
```

### on_drop

- **时机**：插件正在被析构
- **用途**：在插件被销毁时执行代码

更多信息见 [`Drop`](https://doc.rust-lang.org/std/ops/trait.Drop.html)。

```rust

Builder::new("<plugin-name>")
  .on_drop(|app| {
    // 插件已被销毁……
  })
```

## 暴露 Rust API

插件在项目 `desktop.rs` 和 `mobile.rs` 中定义的 API 会以一个与插件同名（Pascal 命名）的结构体导出给使用者。当插件被 setup 时，会创建该结构体的实例并作为 state 托管，这样使用者就可以在任何时候通过 `Manager` 实例（例如 `AppHandle`、`App` 或 `Window`）借助插件中定义的扩展 trait 取到它。

例如，[`global-shortcut` 插件](../../../plugin/11-globalshortcut/)定义了一个 `GlobalShortcut` 结构体，可以通过 `GlobalShortcutExt` trait 的 `global_shortcut` 方法读取：

```rust

tauri::Builder::default()
  .plugin(tauri_plugin_global_shortcut::init())
  .setup(|app| {
    app.global_shortcut().register(...);
    Ok(())
  })
```

## 添加命令

命令定义在 `commands.rs` 文件中。它们就是普通的 Tauri 应用命令，可以直接访问 AppHandle 和 Window 实例、访问 state，并以与应用命令相同的方式接收输入。关于 Tauri 命令的更多细节，请阅读[命令指南](../../3-callingrust/)。

下面这个命令展示了如何通过依赖注入获取 `AppHandle` 和 `Window` 实例，并接收两个输入参数（`on_progress` 和 `url`）：

```rust
use tauri::{command, ipc::Channel, AppHandle, Runtime, Window};

#[command]
async fn upload<R: Runtime>(app: AppHandle<R>, window: Window<R>, on_progress: Channel, url: String) {
  // 在这里实现命令逻辑
  on_progress.send(100).unwrap();
}
```

要把命令暴露给 webview，你必须在 `lib.rs` 中挂接到 `invoke_handler()` 调用：

```rust
    .invoke_handler(tauri::generate_handler![commands::upload])
```

在 `webview-src/index.ts` 中定义一个绑定函数，让插件使用者可以方便地在 JavaScript 中调用该命令：

```js
import { invoke, Channel } from '@tauri-apps/api/core'

export async function upload(url: string, onProgressHandler: (progress: number) => void): Promise<void> {
  const onProgress = new Channel<number>()
  onProgress.onmessage = onProgressHandler
  await invoke('plugin:<plugin-name>|upload', { url, onProgress })
}
```

测试之前请务必先构建 TypeScript 代码。

### 命令权限

默认情况下你的命令不能被前端访问。如果你尝试执行其中之一，会收到拒绝错误的 rejection。
要真正暴露命令，你还需要定义允许每个命令的权限。

#### 权限文件

权限以 JSON 或 TOML 文件的形式定义在 `permissions` 目录中。每个文件都可以定义一组权限、一组权限集以及你插件的默认权限。

##### 权限

权限描述你的插件命令所拥有的特权。它可以允许或拒绝一组命令，并把命令专属作用域和全局作用域关联起来。

```toml

[[permission]]
identifier = "allow-start-server"
description = "Enables the start_server command."
commands.allow = ["start_server"]

[[permission]]
identifier = "deny-start-server"
description = "Denies the start_server command."
commands.deny = ["start_server"]
```

##### 作用域

作用域允许你的插件为单个命令定义更深的限制。
每个权限都可以定义一组作用域对象，用来定义对某个命令专属、或对整个插件全局的允许或拒绝内容。

让我们定义一个示例结构体，用来存放 `shell` 插件被允许启动的二进制文件列表的作用域数据：

```rust
pub struct Entry {
    pub binary: String,
}
```

###### 命令作用域

你的插件使用者可以在自己的能力（capability）文件中为特定命令定义作用域（见[文档](https://tauri.app/reference/acl/scope/)）。
你可以用 [`tauri::ipc::CommandScope`](https://docs.rs/tauri/2.0.0/tauri/ipc/struct.CommandScope.html) 结构体读取命令专属作用域：

```rust
use crate::scope::Entry;

async fn spawn<R: tauri::Runtime>(app: tauri::AppHandle<R>, command_scope: CommandScope<'_, Entry>) -> Result<()> {
  let allowed = command_scope.allows();
  let denied = command_scope.denies();
  todo!()
}
```

###### 全局作用域

当某个权限没有定义任何要允许或拒绝的命令时，它被视为作用域权限，并且只应为你的插件定义全局作用域：

```toml
identifier = "allow-spawn-node"
description = "This scope permits spawning the `node` binary."

[[permission.scope.allow]]
binary = "node"
```

你可以用 [`tauri::ipc::GlobalScope`](https://docs.rs/tauri/2.0.0/tauri/ipc/struct.GlobalScope.html) 结构体读取全局作用域：

```rust
use crate::scope::Entry;

async fn spawn<R: tauri::Runtime>(app: tauri::AppHandle<R>, scope: GlobalScope<'_, Entry>) -> Result<()> {
  let allowed = scope.allows();
  let denied = scope.denies();
  todo!()
}
```

{{% alert title="注意" %}}
为了灵活性，我们建议同时检查全局作用域和命令作用域
{{% /alert %}}

###### Schema

作用域条目需要 `schemars` 依赖来生成 JSON schema，这样插件使用者才能知道作用域的格式，并在 IDE 中获得自动补全。

要定义 schema，请先把依赖添加到 Cargo.toml 文件：

```toml
[dependencies]
schemars = "0.8"

[build-dependencies]
schemars = "0.8"
```

在你的构建脚本中加入以下代码：

```rust
mod scope;

const COMMANDS: &[&str] = &[];

fn main() {
    tauri_plugin::Builder::new(COMMANDS)
        .global_scope_schema(schemars::schema_for!(scope::Entry))
        .build();
}
```

##### 权限集

权限集是单个权限的分组，帮助使用者以更高层次的抽象来管理你的插件。
例如，如果某个 API 使用多个命令，或者一组命令之间存在逻辑关联，你就应当定义一个包含它们的集合：

```toml
[[set]]
identifier = "allow-websocket"
description = "Allows connecting and sending messages through a WebSocket"
permissions = ["allow-connect", "allow-send"]
```

##### 默认权限

默认权限是标识符为 `default` 的特殊权限集。建议你默认启用必需的命令。
例如，如果不允许 `request` 命令，`http` 插件就毫无用处：

```toml
[default]
description = "Allows making HTTP requests"
permissions = ["allow-request"]
```

#### 自动生成权限

为每个命令定义权限最简单的方式，是使用插件构建脚本（`build.rs` 文件）中定义的自动生成选项。
在 `COMMANDS` 常量中，用 snake_case 定义命令列表（应与命令函数名一致），Tauri 会自动生成 `allow-$commandname` 和 `deny-$commandname` 权限。

下面的示例会生成 `allow-upload` 和 `deny-upload` 权限：

```rust

fn main() {
    tauri_plugin::Builder::new(COMMANDS).build();
}
```

更多信息请参阅[权限概述](../../../security/2-permissions/)文档。

## 管理 State

插件可以用与 Tauri 应用相同的方式管理 state。更多信息请阅读[状态管理指南](../../5-statemanagement/)。
