+++
title = "7 Next.js"
date = 2026-09-25T21:31:08+08:00
weight = 7
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/start/frontend/nextjs/](https://tauri.app/start/frontend/nextjs/)

Next.js 是 React 的元框架。你可以在 https://nextjs.org 进一步了解 Next.js。本指南基于 Next.js 14.2.3。

## 检查清单

- 通过设置 `output: 'export'` 使用静态导出。Tauri 不支持基于服务器的方案。
- 在 `tauri.conf.json` 中使用 `out` 目录作为 `frontendDist`。

## 示例配置

1. 更新 Tauri 配置

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```json
{
  "build": {
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build",
    "devUrl": "http://localhost:3000",
    "frontendDist": "../out"
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
    "devUrl": "http://localhost:3000",
    "frontendDist": "../out"
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
    "devUrl": "http://localhost:3000",
    "frontendDist": "../out"
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
    "devUrl": "http://localhost:3000",
    "frontendDist": "../out"
  }
}
```

{{% /tab %}}

{{< /tabpane >}}
2. 更新 Next.js 配置

   ```ts
   // next.config.mjs
   const isProd = process.env.NODE_ENV === 'production';

   const internalHost = process.env.TAURI_DEV_HOST || 'localhost';

   /** @type {import('next').NextConfig} */
   const nextConfig = {
     // 确保 Next.js 使用 SSG 而不是 SSR
     // https://nextjs.org/docs/pages/building-your-application/deploying/static-exports
     output: 'export',
     // 注意：在 SSG 模式下使用 Next.js Image 组件时必须启用此功能。
     // 其它变通方案见 https://nextjs.org/docs/messages/export-image-api 。
     images: {
       unoptimized: true,
     },
     // 配置 assetPrefix，否则服务器无法正确解析你的资源。
     assetPrefix: isProd ? undefined : `http://${internalHost}:3000`,
   };

   export default nextConfig;
   ```

3. 更新 package.json 配置

   ```json
   "scripts": {
     "dev": "next dev",
     "build": "next build",
     "start": "next start",
     "lint": "next lint",
     "tauri": "tauri"
   }
   ```
