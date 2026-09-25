+++
title = "6 Vite"
date = 2026-09-25T21:31:08+08:00
weight = 6
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/start/frontend/vite/](https://tauri.app/start/frontend/vite/)

Vite 是一个构建工具，致力于为现代 Web 项目提供更快、更精简的开发体验。
本指南基于 Vite 8。

## 检查清单

- 在 `src-tauri/tauri.conf.json` 中使用 `../dist` 作为 `frontendDist`。
- 在 iOS 真机上运行时，使用 `process.env.TAURI_DEV_HOST` 作为开发服务器的主机 IP。

## 示例配置

1. 更新 Tauri 配置

   假设你的 `package.json` 中有以下 `dev` 和 `build` 脚本：

   ```json
   {
     "scripts": {
       "dev": "vite",
       "build": "tsc && vite build",
       "preview": "vite preview",
       "tauri": "tauri"
     }
   }
   ```

   你可以配置 Tauri CLI，让它使用你的 Vite 开发服务器和 dist 文件夹，并通过 hooks 自动运行 Vite 脚本：

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```json
{
  "build": {
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build",
    "devUrl": "http://localhost:5173",
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
    "beforeBuildCommand": "yarn build",
    "devUrl": "http://localhost:5173",
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
    "beforeBuildCommand": "pnpm build",
    "devUrl": "http://localhost:5173",
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
    "beforeBuildCommand": "deno task build",
    "devUrl": "http://localhost:5173",
    "frontendDist": "../dist"
  }
}
```

{{% /tab %}}

{{< /tabpane >}}
2. 更新 Vite 配置

   ```js
   import { defineConfig } from 'vite';

   const host = process.env.TAURI_DEV_HOST;

   export default defineConfig({
     // 防止 vite 掩盖 rust 的错误
     clearScreen: false,
     server: {
       // 确保此端口与 tauri.conf.json 文件中 devUrl 的端口一致
       port: 5173,
       // Tauri 期望使用固定端口，若该端口不可用则直接失败
       strictPort: true,
       // 如果设置了 Tauri 期望的 host，就使用它
       host: host || false,
       hmr: host
         ? {
             protocol: 'ws',
             host,
             port: 1421,
           }
         : undefined,

       watch: {
         // 让 vite 忽略对 `src-tauri` 的监听
         ignored: ['**/src-tauri/**'],
       },
     },
     // 以 `envPrefix` 中各项开头的环境变量会通过 `import.meta.env` 暴露在 tauri 的源码中。
     envPrefix: ['VITE_', 'TAURI_ENV_*'],
     build: {
       // Tauri 在 Windows 上使用 Chromium，在 macOS 和 Linux 上使用 WebKit
       target:
         process.env.TAURI_ENV_PLATFORM == 'windows'
           ? 'chrome105'
           : 'safari13',
       // 调试构建不做压缩
       minify: !process.env.TAURI_ENV_DEBUG,
       // 为调试构建生成 sourcemap
       sourcemap: !!process.env.TAURI_ENV_DEBUG,
     },
   });
   ```
