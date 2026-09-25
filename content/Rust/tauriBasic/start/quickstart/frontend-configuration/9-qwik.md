+++
title = "9 Qwik"
date = 2026-09-25T21:31:08+08:00
weight = 9
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/start/frontend/qwik/](https://tauri.app/start/frontend/qwik/)

本指南将带你使用 Qwik Web 框架创建 Tauri 应用。你可以在 https://qwik.dev 进一步了解 Qwik。

## 检查清单

- 使用 [SSG](https://qwik.dev/docs/guides/static-site-generation/)。Tauri 不支持基于服务器的方案。
- 在 `tauri.conf.json` 中使用 `dist/` 作为 `frontendDist`。

## 示例配置

1. 创建一个新的 Qwik 应用

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm create qwik@latest
cd <PROJECT>
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn create qwik@latest
cd <PROJECT>
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm create qwik@latest
cd <PROJECT>
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno run -A npm:create-qwik@latest
cd <PROJECT>
```

{{% /tab %}}

{{< /tabpane >}}
2. 安装 `static adapter`

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm run qwik add static
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn qwik add static
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm qwik add static
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task qwik add static
```

{{% /tab %}}

{{< /tabpane >}}
3. 把 Tauri CLI 添加到你的项目

**包管理器**

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

{{< /tabpane >}}
4. 初始化一个新的 Tauri 项目

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm run tauri init
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

{{< /tabpane >}}
5. Tauri 配置

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```json
// tauri.conf.json
{
  "build": {
    "devUrl": "http://localhost:5173"
    "frontendDist": "../dist",
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build"
  }
}
```

{{% /tab %}}

{{% tab header="yarn" %}}

```json
// tauri.conf.json
{
  "build": {
    "devUrl": "http://localhost:5173"
    "frontendDist": "../dist",
    "beforeDevCommand": "yarn dev",
    "beforeBuildCommand": "yarn build"
  }
}
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```json
// tauri.conf.json
{
  "build": {
    "devUrl": "http://localhost:5173"
    "frontendDist": "../dist",
    "beforeDevCommand": "pnpm dev",
    "beforeBuildCommand": "pnpm build"
  }
}
```

{{% /tab %}}

{{% tab header="deno" %}}

```json
// tauri.conf.json
{
  "build": {
    "devUrl": "http://localhost:5173"
    "frontendDist": "../dist",
    "beforeDevCommand": "deno task dev",
    "beforeBuildCommand": "deno task build"
  }
}
```

{{% /tab %}}

{{< /tabpane >}}
6. 启动你的 `tauri` 应用

**包管理器**

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

{{< /tabpane >}}