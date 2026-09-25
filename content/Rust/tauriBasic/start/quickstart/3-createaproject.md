+++
title = "3 创建项目"
date = 2026-09-25T21:31:08+08:00
weight = 3
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/start/create-project/](https://tauri.app/start/create-project/)

Tauri 之所以如此灵活，原因之一就是它能与几乎所有前端框架配合使用。我们开发了 [`create-tauri-app`](https://github.com/tauri-apps/create-tauri-app) 工具，帮助你使用官方维护的框架模板之一来创建新的 Tauri 项目。

`create-tauri-app` 目前包含 vanilla（不使用框架的 HTML、CSS 和 JavaScript）、[Vue.js](https://vuejs.org)、[Svelte](https://svelte.dev)、[React](https://reactjs.org/)、[SolidJS](https://www.solidjs.com/)、[Angular](https://angular.io/)、[Preact](https://preactjs.com/)、[Yew](https://yew.rs/)、[Leptos](https://github.com/leptos-rs/leptos) 和 [Sycamore](https://sycamore.dev/) 的模板。你也可以在 [Awesome Tauri 仓库](https://github.com/tauri-apps/awesome-tauri)中找到或添加自己的社区模板与框架。

或者，你也可以[把 Tauri 添加到现有项目](#手动配置tauri-cli)，快速把现有代码库变成 Tauri 应用。

## 使用 `create-tauri-app`

要开始使用 `create-tauri-app`，请在你想要创建项目的文件夹中运行下面的一条命令。如果不确定该用哪条命令，我们推荐在 Linux 和 macOS 上使用 Bash 命令，在 Windows 上使用 PowerShell 命令。

{{< tabpane text=true persist=disabled >}}
{{% tab header="Bash" %}}

```sh
sh <(curl https://create.tauri.app/sh)
```

{{% /tab %}}

{{% tab header="PowerShell" %}}

```sh
irm https://create.tauri.app/ps | iex
```

{{% /tab %}}

{{% tab header="Fish" %}}

```sh
sh (curl -sSL https://create.tauri.app/sh | psub)
```

{{% /tab %}}

{{% tab header="npm" %}}

```sh
npm create tauri-app@latest
```

{{% /tab %}}

{{% tab header="Yarn" %}}

```sh
yarn create tauri-app
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm create tauri-app
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno run -A npm:create-tauri-app
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun create tauri-app
```

{{% /tab %}}

{{% tab header="Cargo" %}}

```sh
cargo install create-tauri-app --locked
cargo create-tauri-app
```

{{% /tab %}}

{{< /tabpane >}}
按照提示依次选择项目名称、前端语言、包管理器、前端框架，以及适用时的前端框架选项。

{{% alert title="不确定该选什么？" %}}

我们推荐先从 vanilla 模板（不使用前端框架的 HTML、CSS 和 JavaScript）开始，之后随时可以[集成前端框架](../frontend-configuration/)。

- 选择前端使用哪种语言：`TypeScript / JavaScript`
- 选择包管理器：`pnpm`
- 选择 UI 模板：`Vanilla`
- 选择 UI 风格：`TypeScript`

{{% /alert %}}

#### 脚手架生成新项目

1. 选择名称和 bundle 标识符（应用的唯一 ID）：
   ```
   ? Project name (tauri-app) ›
   ? Identifier (com.tauri-app.app) ›
   ```
2. 为前端选择一种风格。首先是语言：
   ```
   ? Choose which language to use for your frontend ›
   Rust  (cargo)
   TypeScript / JavaScript  (pnpm, yarn, npm, bun)
   .NET  (dotnet)
   ```
3. 选择包管理器（如果有多个可选）：

   **TypeScript / JavaScript** 的选项：

   ```
   ? Choose your package manager ›
   pnpm
   yarn
   npm
   bun
   ```

4. 选择 UI 模板和风格（如果有多个可选）：

   **Rust** 的选项：

   ```
   ? Choose your UI template ›
   Vanilla
   Yew
   Leptos
   Sycamore
   ```

   **TypeScript / JavaScript** 的选项：

   ```
   ? Choose your UI template ›
   Vanilla
   Vue
   Svelte
   React
   Solid
   Angular
   Preact

   ? Choose your UI flavor ›
   TypeScript
   JavaScript
   ```

   **.NET** 的选项：

   ```
   ? Choose your UI template ›
   Blazor  (https://dotnet.microsoft.com/en-us/apps/aspnet/web-apps/blazor/)
   ```

完成后，工具会提示模板已创建，并显示如何使用所配置的包管理器运行它。如果它检测到你的系统缺少某些依赖，会打印出包列表并提示如何安装它们。

#### 启动开发服务器

`create-tauri-app` 完成后，你可以进入项目文件夹、安装依赖，然后使用 [Tauri CLI](https://tauri.app/reference/cli/) 启动开发服务器：

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
cd tauri-app
npm install
npm run tauri dev
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
cd tauri-app
yarn install
yarn tauri dev
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
cd tauri-app
pnpm install
pnpm tauri dev
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
cd tauri-app
deno install
deno task tauri dev
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
cd tauri-app
bun install
bun tauri dev
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo install tauri-cli --version "^2.0.0" --locked
cargo tauri dev
```

{{% /tab %}}

{{< /tabpane >}}
现在你会看到一个新窗口打开，你的应用正在其中运行。

**恭喜！** 你已经做出了自己的 Tauri 应用！🚀

## 手动配置（Tauri CLI）

如果你已有现成的前端，或更愿意自己配置，可以使用 Tauri CLI 单独初始化项目的后端。

{{% alert title="注意" %}}
下面的示例假设你要创建一个新项目。如果你已经初始化了应用的前端，可以跳过第一步。
{{% /alert %}}

1. 为你的项目创建一个新目录并初始化前端。你可以使用纯 HTML、CSS 和 JavaScript，也可以使用任何你喜欢的前端框架，例如 Next.js、Nuxt、Svelte、Yew 或 Leptos。你只需要一种能在浏览器中访问该应用的方式。仅作示例，下面这样配置一个简单的 Vite 应用：

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
mkdir tauri-app
cd tauri-app
npm create vite@latest .
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
mkdir tauri-app
cd tauri-app
yarn create vite .
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
mkdir tauri-app
cd tauri-app
pnpm create vite .
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
mkdir tauri-app
cd tauri-app
deno run -A npm:create-vite .
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
mkdir tauri-app
cd tauri-app
bun create vite
```

{{% /tab %}}

{{< /tabpane >}}
2. 然后，用你选择的包管理器安装 Tauri 的 CLI 工具。如果你使用 `cargo` 安装 Tauri CLI，就必须全局安装它。

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm install -D @tauri-apps/cli@latest
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add -D @tauri-apps/cli@latest
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add -D @tauri-apps/cli@latest
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add -D npm:@tauri-apps/cli@latest
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add -D @tauri-apps/cli@latest
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
   ? Choose your UI template ›
   Vanilla
   Vue
   Svelte
   React
   Solid
   Angular
   Preact

   ? Choose your UI flavor ›
   TypeScript
   JavaScript
```

{{% /tab %}}

{{< /tabpane >}}
3. 确认前端开发服务器的 URL。这就是 Tauri 用来加载内容的 URL。例如，如果你使用 Vite，默认 URL 是 `http://localhost:5173`。

4. 在你的项目目录中初始化 Tauri：

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npx tauri init
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn tauri init
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri init
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri init
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri init
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri init
```

{{% /tab %}}

{{< /tabpane >}}
   运行命令后会显示提示，询问你各种选项：

   ```sh
   ✔ What is your app name? tauri-app
   ✔ What should the window title be? tauri-app
   ✔ Where are your web assets located? ..
   ✔ What is the url of your dev server? http://localhost:5173
   ✔ What is your frontend dev command? pnpm run dev
   ✔ What is your frontend build command? pnpm run build
   ```

   这会在你的项目中创建一个 `src-tauri` 目录，其中包含必要的 Tauri 配置文件。

5. 在 `vite.config.ts` 中配置 `server.watch.ignored` 选项，避免 Vite 监听 `src-tauri` 目录：

   ```js
   import { defineConfig } from "vite";

   export default defineConfig({
     server: {
       watch: {
         ignored: ["**/src-tauri/**"],
       },
     },
   });
   ```

6. 运行开发服务器，验证 Tauri 应用可以正常工作：

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npx tauri dev
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
   该命令会编译 Rust 代码，并打开一个窗口显示你的 Web 内容。

**恭喜！** 你已经使用 Tauri CLI 创建了一个新的 Tauri 项目！🚀

## 后续步骤

- [了解项目结构以及每个文件的作用](../4-projectstructure/)
- [添加并配置前端框架](../frontend-configuration/)
- [Tauri 命令行界面（CLI）参考](https://tauri.app/reference/cli/)
- [学习如何开发你的 Tauri 应用](../../develop/1-overview/)
- [探索更多扩展 Tauri 的功能](../../plugin/1-overview/)
