+++
title = "3 从 Tauri 2.0 Beta 升级"
date = 2026-09-25T21:31:08+08:00
weight = 3
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/start/migrate/from-tauri-2-beta/](https://tauri.app/start/migrate/from-tauri-2-beta/)

本指南将带你把自己的 Tauri 2.0 beta 应用升级到 Tauri 2.0 候选发布版。

## 自动迁移

Tauri v2 CLI 提供了 `migrate` 命令，可以自动完成大部分迁移流程，并帮助你完成剩余工作：

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm install @tauri-apps/cli@latest
npm run tauri migrate
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn upgrade @tauri-apps/cli@latest
yarn tauri migrate
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm update @tauri-apps/cli@latest
pnpm tauri migrate
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri migrate
```

{{% /tab %}}

{{< /tabpane >}}
在[命令行界面参考](https://tauri.app/reference/cli/#migrate)中进一步了解 `migrate` 命令。

## 破坏性变更

从 beta 到候选发布版，我们做了一些破坏性变更。这些变更既可以自动迁移（见上文），也可以手动完成。

### Tauri 核心插件

我们修改了在能力（capabilities）中引用 Tauri 内置插件的方式 [PR #10390](https://github.com/tauri-apps/tauri/pull/10390)。

若要从最新的 beta 版本迁移，你需要在能力（capabilities）中为所有核心权限标识符加上 `core:` 前缀，或者改用 `core:default` 权限并移除旧的核心插件标识符。

```json
"permissions": [
    "path:default",
    "event:default",
    "window:default",
    "app:default",
    "image:default",
    "resources:default",
    "menu:default",
    "tray:default",
]
...
```

```json
"permissions": [
    "core:path:default",
    "core:event:default",
    "core:window:default",
    "core:app:default",
    "core:image:default",
    "core:resources:default",
    "core:menu:default",
    "core:tray:default",
]
...
```

我们还新增了一个特殊的 `core:default` 权限集，它包含所有核心插件的全部默认权限，因此你可以简化能力（capabilities）配置中的权限样板代码。

```json
"permissions": [
    "core:default"
]
...
```

### 内置开发服务器

我们对内置开发服务器的网络暴露方式做了修改 [PR #10437](https://github.com/tauri-apps/tauri/pull/10437) 和 [PR #10456](https://github.com/tauri-apps/tauri/pull/10456)。

内置的移动端开发服务器不再在整个网络上暴露，而是把流量从本地机器直接隧道传输到设备。

目前在 iOS 设备上运行（无论是直接运行还是从 Xcode 运行）时，这项改进还不会自动生效。这种情况下我们默认使用开发服务器的公网地址，但有一个绕过的办法：打开 Xcode 自动建立 macOS 机器与已连接 iOS 设备之间的连接，然后运行 `tauri ios dev --force-ip-prompt` 来选择 iOS 设备的 TUN 地址（以 **::2** 结尾）。

如果你的开发服务器配置打算在真实 iOS 设备上运行，就需要适配这一变更。以前我们建议检查 `TAURI_ENV_PLATFORM` 环境变量是否匹配 `android` 或 `ios`，但既然现在除非使用 iOS 设备都可以连接到 localhost，你应该改为检查 `TAURI_DEV_HOST` 环境变量。下面是一个 Vite 配置迁移的示例：

- 2.0.0-beta：

```js
import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import { internalIpV4Sync } from 'internal-ip';

const mobile = !!/android|ios/.exec(process.env.TAURI_ENV_PLATFORM);

export default defineConfig({
  plugins: [svelte()],
  clearScreen: false,
  server: {
    host: mobile ? '0.0.0.0' : false,
    port: 1420,
    strictPort: true,
    hmr: mobile
      ? {
          protocol: 'ws',
          host: internalIpV4Sync(),
          port: 1421,
        }
      : undefined,
  },
});
```

- 2.0.0：

```js
import { defineConfig } from 'vite';
import Unocss from 'unocss/vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

const host = process.env.TAURI_DEV_HOST;

export default defineConfig({
  plugins: [svelte()],
  clearScreen: false,
  server: {
    host: host || false,
    port: 1420,
    strictPort: true,
    hmr: host
      ? {
          protocol: 'ws',
          host: host,
          port: 1430,
        }
      : undefined,
  },
});
```

{{% alert title="注意" %}}
不再需要 `internal-ip` 这个 NPM 包，你可以直接使用 TAURI_DEV_HOST 的值。
{{% /alert %}}
