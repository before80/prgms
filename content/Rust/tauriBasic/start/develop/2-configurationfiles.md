+++
title = "2 配置文件"
date = 2026-09-25T21:31:08+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/configuration-files/](https://tauri.app/develop/configuration-files/)

由于 Tauri 是构建应用的框架，配置项目设置时可能涉及许多文件。你可能会遇到的一些常见文件有 `tauri.conf.json`、`package.json` 和 `Cargo.toml`。本页会简要说明每一个，帮助你在需要修改时找对文件。

## Tauri 配置

Tauri 配置用于定义 Web 应用的来源、描述应用元数据、配置打包、设置插件配置，以及通过配置窗口、托盘图标、菜单等来修改运行时行为。

该文件由 Tauri 运行时和 Tauri CLI 使用。你可以定义构建设置（例如 [`tauri build` 之前运行的命令](https://tauri.app/reference/config/#beforebuildcommand)或 [`tauri dev`](https://tauri.app/reference/config/#beforedevcommand-1) 启动时的命令）、设置[应用名称](https://tauri.app/reference/config/#productname)和[版本](https://tauri.app/reference/config/#version)、[控制 Tauri 运行时](https://tauri.app/reference/config/#appconfig)，以及[配置插件](https://tauri.app/reference/config/#plugins)。

{{% alert title="提示" %}}
所有可选项都可以在[配置参考](https://tauri.app/reference/config/)中找到。
{{% /alert %}}

### 支持的格式

Tauri 配置的默认格式是 JSON。可以通过在 `Cargo.toml` 中为 `tauri` 和 `tauri-build` 依赖添加 `config-json5` 或 `config-toml` 特性标志（分别对应），来启用 JSON5 或 TOML 格式。

```toml
tauri-build = { version = "2.0.0", features = [ "config-json5" ] }

[dependencies]
tauri = { version = "2.0.0", features = [  "config-json5" ] }
```

所有格式的结构与取值都相同，但格式风格应与相应文件的格式保持一致：

```json5
{
  build: {
    devUrl: 'http://localhost:3000',
    // 启动开发服务器
    beforeDevCommand: 'npm run dev',
  },
  bundle: {
    active: true,
    icon: ['icons/app.png'],
  },
  app: {
    windows: [
      {
        title: 'MyApp',
      },
    ],
  },
  plugins: {
    updater: {
      pubkey: 'updater pub key',
      endpoints: ['https://my.app.updater/{{target}}/{{current_version}}'],
    },
  },
}
```

```toml
dev-url = "http://localhost:3000"
# 启动开发服务器
before-dev-command = "npm run dev"

[bundle]
active = true
icon = ["icons/app.png"]

[[app.windows]]
title = "MyApp"

[plugins.updater]
pubkey = "updater pub key"
endpoints = ["https://my.app.updater/{{target}}/{{current_version}}"]
```

注意 JSON5 和 TOML 支持注释，而 TOML 还可以对配置名使用更符合习惯的 kebab-case。三种格式中字段名都区分大小写。

### 平台特定配置

除了默认配置文件之外，Tauri 还可以从以下位置读取平台特定配置：

- Linux：`tauri.linux.conf.json` 或 `Tauri.linux.toml`
- Windows：`tauri.windows.conf.json` 或 `Tauri.windows.toml`
- macOS：`tauri.macos.conf.json` 或 `Tauri.macos.toml`
- Android：`tauri.android.conf.json` 或 `Tauri.android.toml`
- iOS：`tauri.ios.conf.json` 或 `Tauri.ios.toml`

平台特定配置文件会按照 [JSON Merge Patch (RFC 7396)](https://datatracker.ietf.org/doc/html/rfc7396) 规范与主配置对象合并。

{{% alert title="注意" %}}
对象按键逐个合并，但数组是整体替换，包括嵌套在对象中的数组。
在下面的示例中，`bundle` 会被合并，而 `bundle.resources` 会被替换：平台特定的条目不是扩展基础列表，而是取而代之。
当数组元素是对象时也是如此，例如 `app.windows`。平台特定的条目会替换基础条目，而不是合并进它，因此你省略的任何字段都会回退到默认值，而不是你基础配置中的值。
你想保留的内容需要全部重复一遍。
{{% /alert %}}

例如，给定下面这个基础 `tauri.conf.json`：

```json
{
  "productName": "MyApp",
  "bundle": {
    "resources": ["./resources", "./shared-assets"]
  },
  "plugins": {
    "deep-link": {}
  }
}
```

以及给定的 `tauri.linux.conf.json`：

```json
{
  "productName": "my-app",
  "bundle": {
    "resources": ["./linux-assets"]
  },
  "plugins": {
    "cli": {
      "description": "My app",
      "subcommands": {
        "update": {}
      }
    },
    "deep-link": {}
  }
}
```

Linux 上解析后的配置将是下面这个对象：

```json
{
  "productName": "my-app",
  "bundle": {
    "resources": ["./linux-assets"]
  },
  "plugins": {
    "cli": {
      "description": "My app",
      "subcommands": {
        "update": {}
      }
    },
    "deep-link": {}
  }
}
```

此外，你还可以通过 CLI 提供要合并的配置，更多信息见下一节。

### 扩展配置

Tauri CLI 允许你在运行 `dev`、`android dev`、`ios dev`、`build`、`android build`、`ios build` 或 `bundle` 命令之一时扩展 Tauri 配置。
配置扩展可以通过 `--config` 参数提供，既可以是原始 JSON 字符串，也可以是 JSON 文件的路径。
Tauri 使用 [JSON Merge Patch (RFC 7396)](https://datatracker.ietf.org/doc/html/rfc7396) 规范把所提供的配置值与最初解析出的配置对象合并。

这个机制可以用来定义应用的多个变体，或者在配置应用打包时获得更大的灵活性。

例如，要分发一个完全隔离的 _beta_ 应用，你可以用这个特性配置不同的应用名和标识符：

```json
{
  "productName": "My App Beta",
  "identifier": "com.myorg.myappbeta"
}
```

而要分发这个独立的 _beta_ 应用，你在构建时提供这个配置文件：

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm run tauri build -- --config src-tauri/tauri.beta.conf.json
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri build --config src-tauri/tauri.beta.conf.json
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri build --config src-tauri/tauri.beta.conf.json
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri build --config src-tauri/tauri.beta.conf.json
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri build --config src-tauri/tauri.beta.conf.json
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri build --config src-tauri/tauri.beta.conf.json
```

{{% /tab %}}

{{< /tabpane >}}
## `Cargo.toml`

Cargo 的清单文件用于声明你的应用依赖的 Rust crate、应用元数据以及其它与 Rust 相关的特性。如果你不打算用 Rust 为应用做后端开发，可能不会怎么修改它，但知道它存在以及它做什么很重要。

下面是一个 Tauri 项目最简 `Cargo.toml` 文件的示例：

```toml
name = "app"
version = "0.1.0"
description = "A Tauri App"
authors = ["you"]
license = ""
repository = ""
default-run = "app"
edition = "2021"
rust-version = "1.57"

[build-dependencies]
tauri-build = { version = "2.0.0" }

[dependencies]
serde_json = "1.0"
serde = { version = "1.0", features = ["derive"] }
tauri = { version = "2.0.0", features = [ ] }
```

最需要注意的部分是 `tauri-build` 和 `tauri` 依赖。一般来说，它们都应当与 Tauri CLI 处于相同的最新次要版本，但并非严格要求。如果你在尝试运行应用时遇到问题，应当检查所有 Tauri 版本（`tauri` 和 `tauri-cli`）是否处于各自次要版本的最新版。

Cargo 版本号遵循[语义化版本](https://semver.org)。在 `src-tauri` 文件夹中运行 `cargo update` 会拉取所有依赖可用的最新、Semver 兼容版本。例如，如果你为 `tauri-build` 指定版本 `2.0.0`，Cargo 会检测并下载 `2.0.1`，因为它是可用的最新 Semver 兼容版本。每当引入破坏性变更时，Tauri 都会提升主版本号，这意味着你总是可以安全地升级到最新的次要版本和补丁版本，而不用担心代码被破坏。

如果你想使用某个特定的 crate 版本，可以在依赖版本号前加上 `=` 来改为精确版本：

```
tauri-build = { version = "=2.0.0" }
```

另外需要注意的是 `tauri` 依赖中的 `features=[]` 部分。运行 `tauri dev` 和 `tauri build` 会根据你的 Tauri 配置自动管理项目中需要启用哪些特性。关于 `tauri` 特性标志的更多信息，请参阅[文档](https://docs.rs/tauri/2.0.0/tauri/#cargo-features)。

构建应用时会生成 `Cargo.lock` 文件。该文件主要用于确保开发过程中不同机器上使用相同的依赖（类似于 Node.js 中的 `yarn.lock`、`pnpm-lock.yaml` 或 `package-lock.json`）。建议把这个文件提交到源代码仓库，以获得一致的构建。

要进一步了解 Cargo 清单文件，请参阅[官方文档](https://doc.rust-lang.org/cargo/reference/manifest.html)。

## `package.json`

这是 Node.js 使用的包文件。如果你的 Tauri 应用前端使用基于 Node.js 的技术（例如 `npm`、`yarn` 或 `pnpm`）开发，该文件用于配置前端依赖和脚本。

一个 Tauri 项目最简 `package.json` 文件的示例大致如下：

```json
{
  "scripts": {
    "dev": "command to start your app development mode",
    "build": "command to build your app frontend",
    "tauri": "tauri"
  },
  "dependencies": {
    "@tauri-apps/api": "^2.0.0",
    "@tauri-apps/cli": "^2.0.0"
  }
}
```

通常在 `"scripts"` 部分存放用于启动和构建 Tauri 应用前端的命令。上面的 `package.json` 文件指定了 `dev` 命令（你可以用 `yarn dev` 或 `npm run dev` 运行，以启动前端框架）和 `build` 命令（你可以用 `yarn build` 或 `npm run build` 运行，以构建前端的 Web 资源，供 Tauri 在生产环境打包）。使用这些脚本最方便的方式是通过 Tauri 配置的 [beforeDevCommand](https://tauri.app/reference/config/#beforedevcommand-1) 和 [beforeBuildCommand](https://tauri.app/reference/config/#beforebuildcommand) 钩子把它们接入 Tauri CLI：

```json
{
  "build": {
    "beforeDevCommand": "yarn dev",
    "beforeBuildCommand": "yarn build"
  }
}
```

{{% alert title="注意" %}}
只有在使用 `npm` 时才需要 `"tauri"` 脚本。
{{% /alert %}}

dependencies 对象指定了当你运行 `yarn`、`pnpm install` 或 `npm install` 时 Node.js 应下载哪些依赖（此处是 Tauri CLI 和 API）。

除了 `package.json` 文件，你可能还会看到 `yarn.lock`、`pnpm-lock.yaml` 或 `package-lock.json` 文件。这些文件有助于确保你之后下载依赖时得到与开发期间完全相同的版本（类似于 Rust 中的 `Cargo.lock`）。

要进一步了解 `package.json` 的文件格式，请参阅[官方文档](https://docs.npmjs.com/cli/v8/configuring-npm/package-json)。
