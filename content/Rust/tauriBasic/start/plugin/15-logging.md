+++
title = "15 Logging"
date = 2026-09-25T21:31:08+08:00
weight = 15
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/logging/](https://tauri.app/plugin/logging/)

为你的 Tauri 应用提供可配置的日志功能。

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
npm run tauri add log
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add log
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add log
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add log
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add log
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add log
```

{{% /tab %}}

{{< /tabpane >}}

{{% /tab %}}

{{% tab header="手动" %}}

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-log
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_log::init())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-log
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-log
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-log
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-log
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-log
```

{{% /tab %}}

{{< /tabpane >}}

{{% /tab %}}

{{< /tabpane >}}

## 用法

1. 首先，你需要向 Tauri 注册该插件。

   ```rust
   use tauri_plugin_log::{Target, TargetKind};

   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .plugin(tauri_plugin_log::Builder::new().build())
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

2. 之后，该插件的所有 API 都可以通过 JavaScript 端绑定使用：

   ```javascript
   import {
     warn,
     debug,
     trace,
     info,
     error,
     attachConsole,
     attachLogger,
   } from '@tauri-apps/plugin-log';
   // 使用 `"withGlobalTauri": true` 时，你可以这样写
   // const { warn, debug, trace, info, error, attachConsole, attachLogger } = window.__TAURI__.log;
   ```

## 记录日志

**语言**

{{< tabpane text=true persist=disabled >}}

{{% tab header="JavaScript" %}}

使用该插件的 `warn`、`debug`、`trace`、`info` 或 `error` API 之一，从 JavaScript 代码产生一条日志记录：

```js
import { warn, debug, trace, info, error } from '@tauri-apps/plugin-log';

trace('Trace');
info('Info');
error('Error');
```

要把所有 `console` 消息自动转发给 log 插件，你可以重写它们：

```ts
import { warn, debug, trace, info, error } from '@tauri-apps/plugin-log';

function forwardConsole(
  fnName: 'log' | 'debug' | 'info' | 'warn' | 'error',
  logger: (message: string) => Promise<void>
) {
  const original = console[fnName];
  console[fnName] = (message) => {
    original(message);
    logger(message);
  };
}

forwardConsole('log', trace);
forwardConsole('debug', debug);
forwardConsole('info', info);
forwardConsole('warn', warn);
forwardConsole('error', error);
```

{{% /tab %}}

{{% tab header="Rust" %}}

要在 Rust 侧创建你自己的日志，可以使用 [`log` crate](https://crates.io/crates/log)：

```rust
log::error!("something bad happened!");
log::info!("Tauri is awesome!");
```

注意必须把 [`log` crate](https://crates.io/crates/log) 加入你的 `Cargo.toml` 文件：

```toml
[dependencies]
log = "0.4"
```

{{% /tab %}}

{{< /tabpane >}}

## 日志目标

log 插件的 builder 提供了 `targets` 函数，让你可以配置所有应用日志的常见去处。

{{% alert title="注意" %}}
默认情况下，插件会把日志写到 stdout 以及应用日志目录中的一个文件。
要只使用你自己的日志目标，请调用 `clear_targets`：

```rust
tauri_plugin_log::Builder::new()
.clear_targets()
.build()
```

{{% /alert %}}

### 把日志打印到终端

要把所有日志转发到终端，请启用 `Stdout` 或 `Stderr` 目标：

```rust
tauri_plugin_log::Builder::new()
  .target(tauri_plugin_log::Target::new(
    tauri_plugin_log::TargetKind::Stdout,
  ))
  .build()
```

该目标默认启用。

### 把日志输出到 webview 控制台

要在 webview 控制台中查看所有 Rust 日志，请启用 `Webview` 目标，并 在前端运行 `attachConsole`：

```rust
tauri_plugin_log::Builder::new()
  .target(tauri_plugin_log::Target::new(
    tauri_plugin_log::TargetKind::Webview,
  ))
  .build()
```

```js
import { attachConsole } from '@tauri-apps/plugin-log';
const detach = await attachConsole();
// 如果你不想再把日志打印到控制台，请调用 detach()
```

### 持久化日志

要把所有日志写入文件，你可以使用 `LogDir` 或 `Folder` 目标。

- `LogDir`：

```rust
tauri_plugin_log::Builder::new()
  .target(tauri_plugin_log::Target::new(
    tauri_plugin_log::TargetKind::LogDir {
      file_name: Some("logs".to_string()),
    },
  ))
  .build()
```

使用 LogDir 目标时，所有日志都存储在推荐的日志目录中。下表描述了各平台日志的位置：

| 平台 | 取值                                                                                    | 示例                                           |
| -------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Linux    | `$XDG_DATA_HOME/{bundleIdentifier}/logs` 或 `$HOME/.local/share/{bundleIdentifier}/logs` | `/home/alice/.local/share/com.tauri.dev/logs`     |
| macOS    | `{homeDir}/Library/Logs/{bundleIdentifier}`                                              | `/Users/Alice/Library/Logs/com.tauri.dev`         |
| Windows  | `{FOLDERID_LocalAppData}/{bundleIdentifier}/logs`                                        | `C:\Users\Alice\AppData\Local\com.tauri.dev\logs` |

- `Folder`：

Folder 目标让你可以把日志写到文件系统中的自定义位置。

```rust
tauri_plugin_log::Builder::new()
  .target(tauri_plugin_log::Target::new(
    tauri_plugin_log::TargetKind::Folder {
      path: std::path::PathBuf::from("/path/to/logs"),
      file_name: None,
    },
  ))
  .build()
```

默认的 `file_name` 是应用名称。

#### 配置日志文件行为

默认情况下，日志文件达到最大体积后会被丢弃。
最大文件体积可以通过 builder 的 `max_file_size` 函数配置：

```rust
tauri_plugin_log::Builder::new()
  .max_file_size(50_000 /* 字节 */)
  .build()
```

Tauri 可以在日志文件达到体积上限时自动轮转，而不是丢弃之前的文件。
该行为可以通过 `rotation_strategy` 配置：

```rust
tauri_plugin_log::Builder::new()
  .rotation_strategy(tauri_plugin_log::RotationStrategy::KeepAll)
  .build()
```

### 过滤

默认情况下**所有**日志都会被处理。有一些机制可以减少日志量，只过滤出相关信息。

### 最大日志级别

要设置最大日志级别，请使用 `level` 函数：

```rust
tauri_plugin_log::Builder::new()
  .level(log::LevelFilter::Info)
  .build()
```

在这个示例中，debug 和 trace 日志会被丢弃，因为它们的级别低于 _info_。

也可以为各个模块分别定义最大级别：

```rust
tauri_plugin_log::Builder::new()
  .level(log::LevelFilter::Info)
  // 只为 commands 模块输出详细日志
  .level_for("my_crate_name::commands", log::LevelFilter::Trace)
  .build()
```

注意这些 API 使用 [`log` crate](https://crates.io/crates/log)，必须把它加入你的 `Cargo.toml` 文件：

```toml
[dependencies]
log = "0.4"
```

### 目标过滤

可以定义一个 `filter` 函数，通过检查日志的元数据来丢弃不需要的日志：

```rust
tauri_plugin_log::Builder::new()
  // 排除目标为 `"hyper"` 的日志
  .filter(|metadata| metadata.target() != "hyper")
  .build()
```

### 格式化

log 插件把每条日志记录格式化为 `DATE[TARGET][LEVEL] MESSAGE`。
可以通过 `format` 提供自定义格式化函数：

```rust
tauri_plugin_log::Builder::new()
  .format(|out, message, record| {
    out.finish(format_args!(
      "[{} {}] {}",
      record.level(),
      record.target(),
      message
    ))
  })
  .build()
```

### 为不同目标应用不同格式

你可以通过在 `tauri_plugin_log::Target` 上使用 `format` 方法，为特定目标指定自己的日志格式。
你可能还想在 builder 上调用 `clear_format` 来移除应用到所有目标的默认格式化器：

```rust
tauri_plugin_log::Builder::new()
    .clear_format()
    .targets([
        tauri_plugin_log::Target::new(
            tauri_plugin_log::TargetKind::Stdout
        )
        .format(move |out, message, record| {
            // stdout 的自定义格式化器
        }),
        tauri_plugin_log::Target::new(
            tauri_plugin_log::TargetKind::LogDir { file_name: None }
        )
        .format(move |out, message, record| {
            // 日志文件的自定义格式化器
        }),
    ])
    .build(),
```

#### 日志日期

默认情况下，log 插件使用 UTC 时区格式化日期，
但你可以用 `timezone_strategy` 把它配置为使用本地时区：

```rust
tauri_plugin_log::Builder::new()
  .timezone_strategy(tauri_plugin_log::TimezoneStrategy::UseLocal)
  .build()
```

## 权限

默认情况下，所有有潜在危险的插件命令和作用域都被阻止，无法访问。你必须在 `capabilities` 配置中修改权限才能启用它们。

更多信息请参阅[能力概述](../../security/4-capabilities/)，以及[使用插件权限的分步指南](../../learn/security/1-usingpluginpermissions/)。

```json
{
  "permissions": [
    ...,
    "log:default"
  ]
}
```
