+++
title = "5 CLI"
date = 2026-09-25T21:31:08+08:00
weight = 5
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/cli/](https://tauri.app/plugin/cli/)

Tauri 通过 [clap](https://github.com/clap-rs/clap)（一个健壮的命令行参数解析器）让你的应用拥有 CLI。只要在 `tauri.conf.json` 文件中简单地定义 CLI，你就可以定义自己的接口，并在 JavaScript 和／或 Rust 中读取它的参数匹配映射。

- Windows
  - 由于操作系统限制，生产应用默认无法把文本写回调用它的控制台。变通办法请见 [tauri#8305](https://github.com/tauri-apps/tauri/issues/8305#issuecomment-1826871949)。

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
npm run tauri add cli
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add cli
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add cli
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add cli
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add cli
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add cli
```

{{% /tab %}}

{{< /tabpane >}}

### 手动

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-cli --target 'cfg(any(target_os = "macos", windows, target_os = "linux"))'
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
       tauri::Builder::default()
           .setup(|app| {
               #[cfg(desktop)]
               app.handle().plugin(tauri_plugin_cli::init());
               Ok(())
           })
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-cli
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-cli
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-cli
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-cli
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-cli
```

{{% /tab %}}

{{< /tabpane >}}


## 基础配置

在 `tauri.conf.json` 下，你可以用以下结构配置该接口：

```json
{
  "plugins": {
    "cli": {
      "description": "Tauri CLI Plugin Example",
      "args": [
        {
          "short": "v",
          "name": "verbose",
          "description": "Verbosity level"
        }
      ],
      "subcommands": {
        "run": {
          "description": "Run the application",
          "args": [
            {
              "name": "debug",
              "description": "Run application in debug mode"
            },
            {
              "name": "release",
              "description": "Run application in release mode"
            }
          ]
        }
      }
    }
  }
}
```

{{% alert title="注意" %}}

这里所有的 JSON 配置都只是示例，为清晰起见省略了许多其它字段。

{{% /alert %}}

## 添加参数

`args` 数组表示其所属命令或子命令接受的参数列表。

### 位置参数

位置参数由它在参数列表中的位置来识别。使用以下配置：

```json
{
  "args": [
    {
      "name": "source",
      "index": 1,
      "takesValue": true
    },
    {
      "name": "destination",
      "index": 2,
      "takesValue": true
    }
  ]
}
```

用户可以以 `./app tauri.txt dest.txt` 运行你的应用，参数匹配映射会把 `source` 定义为 `"tauri.txt"`，把 `destination` 定义为 `"dest.txt"`。

### 具名参数

具名参数是一个（键, 值）对，其中键用来标识该值。使用以下配置：

```json
{
  "args": [
    {
      "name": "type",
      "short": "t",
      "takesValue": true,
      "multiple": true,
      "possibleValues": ["foo", "bar"]
    }
  ]
}
```

用户可以以 `./app --type foo bar`、`./app -t foo -t bar` 或 `./app --type=foo,bar` 运行你的应用，参数匹配映射会把 `type` 定义为 `["foo", "bar"]`。

### 标志参数

标志参数是一个独立的键，它的出现与否为你的应用提供信息。使用以下配置：

```json
{
  "args": [
    {
      "name": "verbose",
      "short": "v"
    }
  ]
}
```

用户可以以 `./app -v -v -v`、`./app --verbose --verbose --verbose` 或 `./app -vvv` 运行你的应用，参数匹配映射会把 `verbose` 定义为 `true`，且 `occurrences = 3`。

## 子命令

有些 CLI 应用还有作为子命令的附加接口。例如 `git` CLI 有 `git branch`、`git commit` 和 `git push`。你可以用 `subcommands` 数组定义额外的嵌套接口：

```json
{
  "cli": {
    ...
    "subcommands": {
      "branch": {
        "args": []
      },
      "push": {
        "args": []
      }
    }
  }
}
```

它的配置与根应用配置相同，包含 `description`、`longDescription`、`args` 等。

## 用法

CLI 插件在 JavaScript 和 Rust 中都可以使用。

**语言**

{{< tabpane text=true persist=disabled >}}

{{% tab header="JavaScript" %}}

```javascript
import { getMatches } from '@tauri-apps/plugin-cli';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { getMatches } = window.__TAURI__.cli;

const matches = await getMatches();
if (matches.subcommand?.name === 'run') {
  // 执行了 `./your-app run $ARGS`
  const args = matches.subcommand.matches.args;
  if (args.debug?.value === true) {
    // 执行了 `./your-app run --debug`
  }
  if (args.release?.value === true) {
    // 执行了 `./your-app run --release`
  }
}
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
use tauri_plugin_cli::CliExt;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
   tauri::Builder::default()
       .plugin(tauri_plugin_cli::init())
       .setup(|app| {
           match app.cli().matches() {
               // 这里的 `matches` 是包含 { args, subcommand } 的结构体。
               // `args` 是 `HashMap<String, ArgData>`，`ArgData` 是含 { value, occurrences } 的结构体。
               // `subcommand` 是 `Option<Box<SubcommandMatches>>`，`SubcommandMatches` 是含 { name, matches } 的结构体。
               Ok(matches) => {
                   println!("{:?}", matches)
               }
               Err(_) => {}
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
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": ["cli:default"]
}
```
