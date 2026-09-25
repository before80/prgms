+++
title = "10 SvelteKit"
date = 2026-09-25T21:31:08+08:00
weight = 10
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/start/frontend/sveltekit/](https://tauri.app/start/frontend/sveltekit/)

SvelteKit 是 Svelte 的元框架。你可以在 https://svelte.dev/ 进一步了解 SvelteKit。本指南基于 SvelteKit 2.20.4 / Svelte 5.25.8。

## 检查清单

- 通过 `static-adapter` 使用 [SSG](https://svelte.dev/docs/kit/adapter-static) 和 [SPA](https://svelte.dev/docs/kit/single-page-apps)。Tauri 不支持基于服务器的方案。
- 如果使用**带预渲染**的 SSG，请注意在应用的构建过程中 `load` 函数无法访问 tauri API。推荐使用 SPA 模式（不带预渲染），这样 `load` 函数只会在 webview 中运行，并能访问 tauri API。
- 在 `tauri.conf.json` 中使用 `build/` 作为 `frontendDist`。

## 示例配置

1. 安装 `@sveltejs/adapter-static`

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm install --save-dev @sveltejs/adapter-static
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add -D @sveltejs/adapter-static
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add -D @sveltejs/adapter-static
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add -D npm:@sveltejs/adapter-static
```

{{% /tab %}}

{{< /tabpane >}}
2. 更新 Tauri 配置

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```json
{
  "build": {
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build",
    "devUrl": "http://localhost:5173",
    "frontendDist": "../build"
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
    "frontendDist": "../build"
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
    "frontendDist": "../build"
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
    "frontendDist": "../build"
  }
}
```

{{% /tab %}}

{{< /tabpane >}}
3. 更新 SvelteKit 配置：

   ```js
   import adapter from '@sveltejs/adapter-static';
   import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

   /** @type {import('@sveltejs/kit').Config} */
   const config = {
     // 预处理器的更多信息见
     // https://svelte.dev/docs/kit/integrations#preprocessors
     preprocess: vitePreprocess(),

     kit: {
       adapter: adapter({
         fallback: 'index.html',
       }),
     },
   };

   export default config;
   ```

4. 禁用 SSR

   最后，我们需要通过添加一个根级 `+layout.ts` 文件（如果不使用 TypeScript，则为 `+layout.js`）来禁用 SSR，内容如下：

   ```ts
   // src/routes/+layout.ts
   export const ssr = false;
   ```

   注意，`static-adapter` 并不要求你为整个应用禁用 SSR，但这样做可以让你使用依赖全局 window 对象的 API（例如 Tauri 的 API），而无需[客户端检查](https://svelte.dev/docs/kit/faq#how-do-i-use-x-with-sveltekit-how-do-i-use-a-client-side-only-library-that-depends-on-document-or-window)。

   此外，如果你更偏好静态站点生成（SSG）而不是单页应用（SPA）模式，可以按照[适配器文档](https://svelte.dev/docs/kit/adapter-static)修改适配器配置和 `+layout.ts`。
