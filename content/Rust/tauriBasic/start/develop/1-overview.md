+++
title = "1 开发概述"
date = 2026-09-25T21:31:08+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/](https://tauri.app/develop/)

现在你已[完成全部准备](../../quickstart/)，可以运行你的 Tauri 应用了。

如果你使用 UI 框架或 JavaScript 打包工具，通常会有一个开发服务器来加速开发流程。因此如果你还没配置应用的开发 URL 和启动脚本，可以通过 [devUrl](https://tauri.app/reference/config/#devurl) 和 [beforeDevCommand](https://tauri.app/reference/config/#beforedevcommand) 配置项来设置：

```json
{
  "build": {
    "devUrl": "http://localhost:3000",
    "beforeDevCommand": "npm run dev"
  }
}
```

{{% alert title="注意" %}}

每个框架都有自己的开发工具。本文档不可能覆盖全部，也无法始终跟上它们的更新。

请参阅你所使用框架的文档，了解详情并确定应配置的正确取值。

{{% /alert %}}

否则，如果你不使用 UI 框架或模块打包工具，可以把 Tauri 指向你的前端源代码，Tauri CLI 会为你启动一个开发服务器：

```json
{
  "build": {
    "frontendDist": "./src"
  }
}
```

注意在这个例子中，`src` 文件夹必须包含一个 `index.html` 文件，以及前端加载的其它资源。

{{% alert title="纯／Vanilla 开发服务器的安全" color="warning" %}}

内置的 Tauri 开发服务器不支持双向认证或加密。绝不要在不受信任的网络中使用它进行开发。
更详细的解释请参阅[开发服务器安全考量](../../security/10-lifecycle/#开发服务器)。

{{% /alert %}}

## 开发桌面应用

要开发桌面端应用，请运行 `tauri dev` 命令。

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm run tauri dev
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri dev
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri dev
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri dev
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri dev
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri dev
```

{{% /tab %}}

{{< /tabpane >}}
第一次运行该命令时，Rust 包管理器可能需要**几分钟**来下载并构建所有必需的包。
由于它们会被缓存，后续构建会快得多，只需重新构建你的代码。

Rust 构建完成后，webview 会打开并显示你的 Web 应用。
你可以修改 Web 应用，如果你的工具支持，webview 会像浏览器一样自动更新。

### 打开 Web 检查器

你可以通过在 webview 上右键并点击 “Inspect”，或在 Windows 和 Linux 上使用 `Ctrl + Shift + I`、在 macOS 上使用 `Cmd + Option + I` 快捷键，打开 Web 检查器来调试应用。

## 开发移动应用

移动端开发与桌面端类似，但你必须改为运行 `tauri android dev` 或 `tauri ios dev`：

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm run tauri [android|ios] dev
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri [android|ios] dev
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri [android|ios] dev
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri [android|ios] dev
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri [android|ios] dev
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri [android|ios] dev
```

{{% /tab %}}

{{< /tabpane >}}
第一次运行该命令时，Rust 包管理器可能需要**几分钟**来下载并构建所有必需的包。
由于它们会被缓存，后续构建会快得多，只需重新构建你的代码。

### 开发服务器

移动端的开发服务器与桌面端类似，但如果你要在 iOS 真机上运行，必须把它配置为监听 Tauri CLI 提供的特定地址，该地址定义在 `TAURI_DEV_HOST` 环境变量中。
这个地址要么是公网地址（默认行为），要么是 iOS 设备实际的 TUN 地址——后者更安全，但目前需要 Xcode 才能连接到设备。

要使用 iOS 设备的地址，你必须在运行 dev 命令之前打开 Xcode，并确保你的设备在 Window > Devices and Simulators 菜单中已通过网络连接。
然后你必须运行 `tauri ios dev --force-ip-prompt` 来选择 iOS 设备地址（一个以 **::2** 结尾的 IPv6 地址）。

要让开发服务器监听正确的主机以便 iOS 设备访问，你必须调整它的配置，在提供了 `TAURI_DEV_HOST` 值时使用该值。下面是 Vite 的示例配置：

```js
import { defineConfig } from 'vite';

const host = process.env.TAURI_DEV_HOST;

// https://vitejs.dev/config/
export default defineConfig({
  clearScreen: false,
  server: {
    host: host || false,
    port: 1420,
    strictPort: true,
    hmr: host
      ? {
          protocol: 'ws',
          host,
          port: 1421,
        }
      : undefined,
  },
});
```

更多信息请查阅你所使用框架的配置指南。

{{% alert title="注意" %}}
用 [create-tauri-app](https://github.com/tauri-apps/create-tauri-app) 创建的项目已经为移动端开发配置好了开发服务器。
{{% /alert %}}

### 选择设备

默认情况下，移动端 dev 命令会尝试在已连接的设备上运行应用，如果失败则提示你选择要使用的模拟器。
要预先指定运行目标，你可以把设备或模拟器名称作为参数传入：

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm run tauri ios dev 'iPhone 15'
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri ios dev 'iPhone 15'
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri ios dev 'iPhone 15'
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri ios dev 'iPhone 15'
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri ios dev 'iPhone 15'
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri ios dev 'iPhone 15'
```

{{% /tab %}}

{{< /tabpane >}}
### 使用 Xcode 或 Android Studio

你也可以选择使用 Xcode 或 Android Studio 来开发应用。
用 IDE 取代命令行工具，有助于排查某些开发问题。
要打开移动端 IDE，而不是在已连接设备或模拟器上运行，请使用 `--open` 标志：

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm run tauri [android|ios] dev --open
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri [android|ios] dev --open
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri [android|ios] dev --open
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri [android|ios] dev --open
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri [android|ios] dev --open
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri [android|ios] dev --open
```

{{% /tab %}}

{{< /tabpane >}}
{{% alert title="注意" %}}
如果你打算在 iOS 真机上运行应用，还必须提供 `--host` 参数，并且你的开发服务器必须把 `process.env.TAURI_DEV_HOST` 的值用作 host。
更多信息请查阅你所使用框架的配置指南。

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm run tauri [android|ios] dev --open --host
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri [android|ios] dev --open --host
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri [android|ios] dev --open --host
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri [android|ios] dev --open --host
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri [android|ios] dev --open --host
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri [android|ios] dev --open --host
```

{{% /tab %}}

{{< /tabpane >}}
{{% /alert %}}

{{% alert title="警告" color="warning" %}}
要使用 Xcode 或 Android Studio，Tauri CLI 进程**必须**保持运行，**不能**被结束。
建议使用 `tauri [android|ios] dev --open` 命令，并在你关闭 IDE 之前保持该进程存活。
{{% /alert %}}

### 打开 Web 检查器

- iOS

  必须使用 Safari 来访问 iOS 应用的 Web 检查器。

  在你的 Mac 上打开 Safari，在菜单栏选择 **Safari > Settings**，点击 **Advanced**，然后勾选 **Show features for web developers**。

  如果你在真机上运行，还必须在 **Settings > Safari > Advanced** 中启用 **Web Inspector**。

  完成以上所有步骤后，你应该会在 Safari 中看到一个 **Develop** 菜单，其中列出了可检查的已连接设备与应用。
  选择你的设备或模拟器，点击 **localhost** 即可打开 Safari 开发者工具窗口。

- Android

  检查器在 Android 模拟器上默认启用，但在真机上必须手动启用。
  把你的 Android 设备连接到电脑，在 Android 设备上打开 **Settings** 应用，选择 **About**，滚动到 Build Number 并连续点击 7 次。
  这会为你的 Android 设备启用开发者模式以及 **Developer Options** 设置。

  要在设备上启用应用调试，你必须进入 **Developer Options** 设置，打开开发者选项开关并启用 **USB Debugging**。

  {{% alert title="注意" %}}
  每个 Android 发行版启用开发者模式的方式各不相同。更多信息请查看你设备厂商的文档。
  {{% /alert %}}

  Android 的 Web 检查器由 Google Chrome 的 DevTools 提供支持，可以在电脑上的 Chrome 浏览器中访问 `chrome://inspect` 打开。
  如果你的 Android 应用正在运行，设备或模拟器应当出现在远程设备列表中，点击与你的设备匹配条目上的 **inspect** 即可打开开发者工具。

### 故障排除

1. 在 Xcode 上运行构建脚本时出错

Tauri 通过创建一个构建阶段来接入 iOS Xcode 项目，该阶段执行 Tauri CLI，把 Rust 源码编译成运行时加载的库。该构建阶段在 Xcode 的进程上下文中执行，因此可能无法使用 PATH 追加之类的 shell 修改，所以在使用 Node.js 版本管理器之类可能不兼容的工具时要小心。

2. 首次执行 iOS 应用时的网络权限提示

当你第一次执行 `tauri ios dev` 时，iOS 可能会提示你授予在本地网络上查找并连接设备的权限。之所以需要该权限，是因为要让 iOS 设备访问你的开发服务器，服务器必须暴露在本地网络上。要在设备上运行应用，你必须点击 Allow 并重启应用。

## 响应源代码变更

与 webview 实时反映变更的方式类似，`tauri dev` 会监视你的 `src-tauri` 文件夹以及工作区中它所依赖的 crate，因此每当你修改它们时，应用都会自动重新构建并重启。

你可以在 `tauri dev` 命令上使用 `--no-watch` 标志来禁用该行为。

要忽略对某些文件的监视，你可以创建 `.taurignore` 文件，它的工作方式与普通的 `.gitignore` 文件相同：

```txt
src/generated/*.rs
deny.toml
```

`.taurignore` 文件通常放在 `src-tauri` 目录或 [cargo 工作区](https://doc.rust-lang.org/cargo/reference/workspaces.html)根文件夹中。
目前，`tauri dev` 会在被监视文件夹与 Cargo 工作区根文件夹的共同祖先目录内查找任意位置的 `.taurignore` 文件。

## 使用浏览器 DevTools

Tauri 的 API 只在你的应用窗口中有效，因此一旦开始使用它们，你就无法再在系统浏览器中打开前端了。

如果你更喜欢使用浏览器的开发者工具，必须配置 [tauri-invoke-http](https://github.com/tauri-apps/tauri-invoke-http)，把 Tauri API 调用通过 HTTP 服务器桥接出去。

## 源代码控制

在你的项目仓库中，你**应当**把 `src-tauri/Cargo.lock` 与 `src-tauri/Cargo.toml` 一起提交到 git，
因为 Cargo 使用锁文件来提供确定性构建。因此，建议所有应用都提交自己的 `Cargo.lock`。你**不应**提交 `src-tauri/target` 文件夹或其任何内容。
