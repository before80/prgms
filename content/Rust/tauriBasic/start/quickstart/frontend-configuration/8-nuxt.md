+++
title = "8 Nuxt"
date = 2026-09-25T21:31:08+08:00
weight = 8
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/start/frontend/nuxt/](https://tauri.app/start/frontend/nuxt/)

Nuxt 是 Vue 的元框架。你可以在 https://nuxt.com 进一步了解 Nuxt。本指南基于 Nuxt 4.2。

## 检查清单

- 通过设置 `ssr: false` 使用 SSG。Tauri 不支持基于服务器的方案。
- 在 `tauri.conf.json` 中使用默认的 `../dist` 作为 `frontendDist`。
- 使用 `nuxi build` 编译。
- （可选）：在 `nuxt.config.ts` 中设置 `telemetry: false` 以禁用遥测。

## 示例配置

1. 更新 Tauri 配置

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```json
{
  "build": {
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run generate",
    "devUrl": "http://localhost:3000",
    "frontendDist": "../dist"
  }
}
```

{{% /tab %}}

{{% tab header="yarn" %}}

```json
{
  "build": {
    "beforeDevCommand": "yarn dev",
    "beforeBuildCommand": "yarn generate",
    "devUrl": "http://localhost:3000",
    "frontendDist": "../dist"
  }
}
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```json
{
  "build": {
    "beforeDevCommand": "pnpm dev",
    "beforeBuildCommand": "pnpm generate",
    "devUrl": "http://localhost:3000",
    "frontendDist": "../dist"
  }
}
```

{{% /tab %}}

{{% tab header="deno" %}}

```json
{
  "build": {
    "beforeDevCommand": "deno task dev",
    "beforeBuildCommand": "deno task generate",
    "devUrl": "http://localhost:3000",
    "frontendDist": "../dist"
  }
}
```

{{% /tab %}}

{{< /tabpane >}}
2. 更新 Nuxt 配置

   ```ts
   export default defineNuxtConfig({
     compatibilityDate: '2025-05-15',
     //（可选）启用 Nuxt 开发者工具
     devtools: { enabled: true },
     // 启用 SSG
     ssr: false,
     // 让开发服务器在 iOS 真机上运行时可以被其它设备发现
     devServer: {
       host: '0',
     },
     vite: {
       // 更好地支持 Tauri CLI 的输出
       clearScreen: false,
       // 启用环境变量
       // 更多环境变量见
       // https://v2.tauri.app/reference/environment-variables/
       envPrefix: ['VITE_', 'TAURI_'],
       server: {
         // Tauri 需要一个固定的端口
         strictPort: true,
       },
     },
     // 避免出现错误 [unhandledRejection] EMFILE: too many open files, watch
     ignore: ['**/src-tauri/**'],
   });
   ```
