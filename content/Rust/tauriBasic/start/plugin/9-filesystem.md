+++
title = "9 File System"
date = 2026-09-25T21:31:08+08:00
weight = 9
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/file-system/](https://tauri.app/plugin/file-system/)

访问文件系统。

{{% alert title="在 Rust 侧使用 std::fs 或 tokio::fs" %}}
如果你想通过 Rust 操作文件／目录，请使用传统 Rust 库（std::fs、tokio::fs 等）。
{{% /alert %}}

## 支持的平台

| 平台 | 支持程度 | 说明 |
| --- | --- | --- |
| Windows | 完整支持 |  |
| Linux | 完整支持 |  |
| macOS | 完整支持 |  |
| Android | 部分支持 |  |
| iOS | 部分支持 |  |

## 设置

安装 fs 插件即可开始。

**安装方式**

{{< tabpane text=true persist=disabled >}}

{{% tab header="自动" %}}

使用你的项目包管理器添加依赖：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm run tauri add fs
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn run tauri add fs
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm tauri add fs
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno task tauri add fs
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun tauri add fs
```

{{% /tab %}}

{{% tab header="cargo" %}}

```sh
cargo tauri add fs
```

{{% /tab %}}

{{< /tabpane >}}

{{% /tab %}}

{{% tab header="手动" %}}

1. 在 `src-tauri` 文件夹中运行以下命令，把插件加入 `Cargo.toml` 里的项目依赖：

   ```sh
   cargo add tauri-plugin-fs
   ```

2. 修改 `lib.rs` 初始化插件：

   ```rust
   #[cfg_attr(mobile, tauri::mobile_entry_point)]
   pub fn run() {
     tauri::Builder::default()
       .plugin(tauri_plugin_fs::init())
       .run(tauri::generate_context!())
       .expect("error while running tauri application");
   }
   ```

3. 用你偏好的 JavaScript 包管理器安装 JavaScript 端绑定：

{{< tabpane text=true persist=disabled >}}

{{% tab header="npm" %}}

```sh
npm install @tauri-apps/plugin-fs
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @tauri-apps/plugin-fs
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @tauri-apps/plugin-fs
```

{{% /tab %}}

{{% tab header="deno" %}}

```sh
deno add npm:@tauri-apps/plugin-fs
```

{{% /tab %}}

{{% tab header="bun" %}}

```sh
bun add @tauri-apps/plugin-fs
```

{{% /tab %}}

{{< /tabpane >}}

{{% /tab %}}

{{< /tabpane >}}

## 配置

### Android

使用 audio、cache、documents、downloads、picture、public 或 video 目录时，你的应用必须能访问外部存储。

把以下权限加入 `gen/android/app/src/main/AndroidManifest.xml` 文件中的 `manifest` 标签：

```xml
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
```

### iOS

Apple 要求应用开发者说明 API 使用的已批准理由，以增强用户隐私。

你必须在 `src-tauri/gen/apple` 文件夹中创建 `PrivacyInfo.xcprivacy` 文件，
其中包含所需的 [NSPrivacyAccessedAPICategoryFileTimestamp](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files/describing_use_of_required_reason_api) 键以及 [C617.1](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files/describing_use_of_required_reason_api) 推荐理由。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>NSPrivacyAccessedAPITypes</key>
    <array>
      <dict>
        <key>NSPrivacyAccessedAPIType</key>
        <string>NSPrivacyAccessedAPICategoryFileTimestamp</string>
        <key>NSPrivacyAccessedAPITypeReasons</key>
        <array>
          <string>C617.1</string>
        </array>
      </dict>
    </array>
  </dict>
</plist>
```

## 用法

fs 插件在 JavaScript 和 Rust 中都可以使用。

{{% alert title="两种不同的 API" color="warning" %}}
虽然该插件在前端提供文件操作 API，但在后端它只提供修改某些资源（文件、目录等）权限的方法。

在 Rust 侧你可以使用传统的文件操作库：
[std::fs](https://doc.rust-lang.org/std/fs/struct.File.html)、[tokio::fs](https://docs.rs/tokio/latest/tokio/fs/index.html) 或其它库。
{{% /alert %}}

**语言**

{{< tabpane text=true persist=disabled >}}

{{% tab header="JavaScript" %}}

```javascript
import { exists, BaseDirectory } from '@tauri-apps/plugin-fs';
// 使用 `"withGlobalTauri": true` 时，你可以这样写
// const { exists, BaseDirectory } = window.__TAURI__.fs;

// 检查 `$APPDATA/avatar.png` 文件是否存在
await exists('avatar.png', { baseDir: BaseDirectory.AppData });
```

{{% /tab %}}

{{% tab header="Rust" %}}

```rust
use tauri_plugin_fs::FsExt;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
  tauri::Builder::default()
      .plugin(tauri_plugin_fs::init())
      .setup(|app| {
          // 允许给定的目录
          let scope = app.fs_scope();
        	scope.allow_directory("/path/to/directory", false);
          dbg!(scope.allowed());

          Ok(())
       })
       .run(tauri::generate_context!())
       .expect("error while running tauri application");
}
```

{{% /tab %}}

{{< /tabpane >}}

## 安全

该模块防止路径穿越，不允许使用父目录访问符
（即不允许 "/usr/path/to/../file" 或 "../path/to/file" 这类路径）。
通过该 API 访问的路径必须相对于某个[基础目录](#路径)，或用[路径 API](#路径)创建。

更多信息请参阅 [@tauri-apps/plugin-fs - Security](https://github.com/tauri-apps/plugins-workspace/blob/v2/plugins/fs/README.md#security)。

## 路径

文件系统插件提供两种操作路径的方式：[基础目录](#路径)和[路径 API](#路径)。

- 基础目录

  每个 API 都有一个 options 参数，让你定义作为该操作工作目录的 [baseDir](#路径)。

  ```js
  import { readFile } from '@tauri-apps/plugin-fs';
  const contents = await readFile('avatars/tauri.png', {
    baseDir: BaseDirectory.Home,
  });
  ```

  在上面的示例中，因为使用了 **Home** 基础目录，所以读取的是 ~/avatars/tauri.png 文件。

- 路径 API

  或者你也可以使用路径 API 进行路径操作。

  ```js
  import { readFile } from '@tauri-apps/plugin-fs';
  import * as path from '@tauri-apps/api/path';
  const home = await path.homeDir();
  const contents = await readFile(await path.join(home, 'avatars/tauri.png'));
  ```

## 文件

### 创建

创建一个文件并返回它的句柄。如果文件已存在，它会被截断。

```js
import { create, BaseDirectory } from '@tauri-apps/plugin-fs';
const file = await create('foo/bar.txt', { baseDir: BaseDirectory.AppData });
await file.write(new TextEncoder().encode('Hello world'));
await file.close();
```

{{% alert title="注意" %}}
操作完文件后请始终调用 `file.close()`。
{{% /alert %}}

### 写入

出于性能考虑，该插件为文本文件和二进制文件分别提供了 API。

- 文本文件

  ```js
  import { writeTextFile, BaseDirectory } from '@tauri-apps/plugin-fs';
  const contents = JSON.stringify({ notifications: true });
  await writeTextFile('config.json', contents, {
    baseDir: BaseDirectory.AppConfig,
  });
  ```

- 二进制文件

  ```js
  import { writeFile, BaseDirectory } from '@tauri-apps/plugin-fs';
  const contents = new Uint8Array(); // 填充一个字节数组
  await writeFile('config', contents, {
    baseDir: BaseDirectory.AppConfig,
  });
  ```

### 打开

打开一个文件并返回它的句柄。
通过这个 API，你可以更好地控制文件的打开方式
（只读模式、只写模式、追加而非覆盖、仅在文件不存在时创建等）。

{{% alert title="注意" %}}
操作完文件后请始终调用 `file.close()`。
{{% /alert %}}

- 只读

  这是默认模式。

  ```js
  import { open, BaseDirectory } from '@tauri-apps/plugin-fs';
  const file = await open('foo/bar.txt', {
    read: true,
    baseDir: BaseDirectory.AppData,
  });

  const stat = await file.stat();
  const buf = new Uint8Array(stat.size);
  await file.read(buf);
  const textContents = new TextDecoder().decode(buf);
  await file.close();
  ```

- 只写

  ```js
  import { open, BaseDirectory } from '@tauri-apps/plugin-fs';
  const file = await open('foo/bar.txt', {
    write: true,
    baseDir: BaseDirectory.AppData,
  });
  await file.write(new TextEncoder().encode('Hello world'));
  await file.close();
  ```

  默认情况下，任何 `file.write()` 调用都会截断文件。
  要了解如何改为追加到已有内容之后，请看下面的示例。

- 追加

  ```js
  import { open, BaseDirectory } from '@tauri-apps/plugin-fs';
  const file = await open('foo/bar.txt', {
    append: true,
    baseDir: BaseDirectory.AppData,
  });
  await file.write(new TextEncoder().encode('world'));
  await file.close();
  ```

  注意 `{ append: true }` 与 `{ write: true, append: true }` 效果相同。

- 截断

  当设置了 `truncate` 选项且文件已存在时，它会被截断为长度 0。

  ```js
  import { open, BaseDirectory } from '@tauri-apps/plugin-fs';
  const file = await open('foo/bar.txt', {
    write: true,
    truncate: true,
    baseDir: BaseDirectory.AppData,
  });
  await file.write(new TextEncoder().encode('world'));
  await file.close();
  ```

  该选项要求 `write` 为 `true`。

  如果你想通过多次 `file.write()` 调用重写一个已有文件，可以将它与 `append` 选项一起使用。

- create

  默认情况下，`open` API 只打开已存在的文件。要在文件不存在时创建它、存在时打开它，
  请把 `create` 设为 `true`：

  ```js
  import { open, BaseDirectory } from '@tauri-apps/plugin-fs';
  const file = await open('foo/bar.txt', {
    write: true,
    create: true,
    baseDir: BaseDirectory.AppData,
  });
  await file.write(new TextEncoder().encode('world'));
  await file.close();
  ```

  为了让文件被创建，`write` 或 `append` 也必须设为 `true`。

  要在文件已存在时报错，请参阅 `createNew`。

- createNew

  `createNew` 与 `create` 类似，但如果文件已存在则会失败。

  ```js
  import { open, BaseDirectory } from '@tauri-apps/plugin-fs';
  const file = await open('foo/bar.txt', {
    write: true,
    createNew: true,
    baseDir: BaseDirectory.AppData,
  });
  await file.write(new TextEncoder().encode('world'));
  await file.close();
  ```

  为了让文件被创建，`write` 也必须设为 `true`。

### 读取

出于性能考虑，该插件为读取文本文件和二进制文件分别提供了 API。

- 文本文件

  ```js
  import { readTextFile, BaseDirectory } from '@tauri-apps/plugin-fs';
  const configToml = await readTextFile('config.toml', {
    baseDir: BaseDirectory.AppConfig,
  });
  ```

  如果文件很大，你可以用 `readTextFileLines` API 流式读取它的各行：

  ```typescript
  import { readTextFileLines, BaseDirectory } from '@tauri-apps/plugin-fs';
  const lines = await readTextFileLines('app.logs', {
    baseDir: BaseDirectory.AppLog,
  });
  for await (const line of lines) {
    console.log(line);
  }
  ```

- 二进制文件

  ```js
  import { readFile, BaseDirectory } from '@tauri-apps/plugin-fs';
  const icon = await readFile('icon.png', {
    baseDir: BaseDirectory.Resources,
  });
  ```

### 删除

调用 `remove()` 删除文件。如果文件不存在，会返回错误。

```js
import { remove, BaseDirectory } from '@tauri-apps/plugin-fs';
await remove('user.db', { baseDir: BaseDirectory.AppLocalData });
```

### 复制

`copyFile` 函数接收源路径和目标路径。
注意你必须分别配置各自的基础目录。

```js
import { copyFile, BaseDirectory } from '@tauri-apps/plugin-fs';
await copyFile('user.db', 'user.db.bk', {
  fromPathBaseDir: BaseDirectory.AppLocalData,
  toPathBaseDir: BaseDirectory.Temp,
});
```

在上面的示例中，\<app-local-data\>/user.db 文件会被复制到 $TMPDIR/user.db.bk。

### 是否存在

使用 `exists()` 函数检查文件是否存在：

```js
import { exists, BaseDirectory } from '@tauri-apps/plugin-fs';
const tokenExists = await exists('token', {
  baseDir: BaseDirectory.AppLocalData,
});
```

### 元数据

文件元数据可以用 `stat` 和 `lstat` 函数获取。
`stat` 会跟随符号链接（如果它指向的真实文件不在作用域允许范围内，则返回错误），
而 `lstat` 不跟随符号链接，返回符号链接自身的信息。

```js
import { stat, BaseDirectory } from '@tauri-apps/plugin-fs';
const metadata = await stat('app.db', {
  baseDir: BaseDirectory.AppLocalData,
});
```

### 重命名

`rename` 函数接收源路径和目标路径。
注意你必须分别配置各自的基础目录。

```js
import { rename, BaseDirectory } from '@tauri-apps/plugin-fs';
await rename('user.db.bk', 'user.db', {
  fromPathBaseDir: BaseDirectory.AppLocalData,
  toPathBaseDir: BaseDirectory.Temp,
});
```

在上面的示例中，\<app-local-data\>/user.db.bk 文件会被重命名为 $TMPDIR/user.db。

### 截断

把指定文件截断或扩展到指定长度（默认 0）。

- 截断到 0 长度

```typescript
import { truncate } from '@tauri-apps/plugin-fs';
await truncate('my_file.txt', 0, { baseDir: BaseDirectory.AppLocalData });
```

- 截断到指定长度

```typescript
import {
  truncate,
  readTextFile,
  writeTextFile,
  BaseDirectory,
} from '@tauri-apps/plugin-fs';

const filePath = 'file.txt';
await writeTextFile(filePath, 'Hello World', {
  baseDir: BaseDirectory.AppLocalData,
});
await truncate(filePath, 7, {
  baseDir: BaseDirectory.AppLocalData,
});
const data = await readTextFile(filePath, {
  baseDir: BaseDirectory.AppLocalData,
});
console.log(data); // "Hello W"
```

## 目录

### 创建

要创建目录，请调用 `mkdir` 函数：

```js
import { mkdir, BaseDirectory } from '@tauri-apps/plugin-fs';
await mkdir('images', {
  baseDir: BaseDirectory.AppLocalData,
});
```

### 读取

`readDir` 函数递归列出目录的条目：

```typescript
import { readDir, BaseDirectory } from '@tauri-apps/plugin-fs';
const entries = await readDir('users', { baseDir: BaseDirectory.AppLocalData });
```

### 删除

调用 `remove()` 删除目录。如果目录不存在，会返回错误。

```js
import { remove, BaseDirectory } from '@tauri-apps/plugin-fs';
await remove('images', { baseDir: BaseDirectory.AppLocalData });
```

如果目录非空，必须把 `recursive` 选项设为 `true`：

```js
import { remove, BaseDirectory } from '@tauri-apps/plugin-fs';
await remove('images', {
  baseDir: BaseDirectory.AppLocalData,
  recursive: true,
});
```

### 是否存在

使用 `exists()` 函数检查目录是否存在：

```js
import { exists, BaseDirectory } from '@tauri-apps/plugin-fs';
const tokenExists = await exists('images', {
  baseDir: BaseDirectory.AppLocalData,
});
```

### 元数据

目录元数据可以用 `stat` 和 `lstat` 函数获取。
`stat` 会跟随符号链接（如果它指向的真实文件不在作用域允许范围内，则返回错误），
而 `lstat` 不跟随符号链接，返回符号链接自身的信息。

```js
import { stat, BaseDirectory } from '@tauri-apps/plugin-fs';
const metadata = await stat('databases', {
  baseDir: BaseDirectory.AppLocalData,
});
```

## 监听变化

要监听目录或文件的变化，请使用 `watch` 或 `watchImmediate` 函数。

- watch

  `watch` 带防抖，因此只会在一定延迟后才发出事件：

  ```js
  import { watch, BaseDirectory } from '@tauri-apps/plugin-fs';
  await watch(
    'app.log',
    (event) => {
      console.log('app.log event', event);
    },
    {
      baseDir: BaseDirectory.AppLog,
      delayMs: 500,
    }
  );
  ```

- watchImmediate

  `watchImmediate` 会立即通知监听器：

  ```js
  import { watchImmediate, BaseDirectory } from '@tauri-apps/plugin-fs';
  await watchImmediate(
    'logs',
    (event) => {
      console.log('logs directory event', event);
    },
    {
      baseDir: BaseDirectory.AppLog,
      recursive: true,
    }
  );
  ```

默认情况下，对目录的监听操作不是递归的。
把 `recursive` 选项设为 `true`，即可递归监听所有子目录的变化。

{{% alert title="注意" %}}
监听函数需要 `watch` 特性标志：

```toml
[dependencies]
tauri-plugin-fs = { version = "2.0.0", features = ["watch"] }
```

{{% /alert %}}

## 权限

默认情况下，所有有潜在危险的插件命令和作用域都被阻止，无法访问。你必须在 `capabilities` 配置中修改权限才能启用它们。

更多信息请参阅[能力概述](../../security/4-capabilities/)，以及[使用权限的分步指南](../../learn/security/1-usingpluginpermissions/)。

{{% alert title="仅有权限并不会授予作用域" color="warning" %}}
仅启用 `fs:allow-exists` 这样的权限**并不会**允许访问任何路径。大多数 `fs` 命令还需要一个**作用域**，明确列出该命令可以访问哪些路径。没有 `allow` 作用域时，调用会在运行时以 `forbidden path` 错误失败，即使权限已启用。

```json
{
  "permissions": ["fs:default", "fs:allow-exists"]
}
```

```json
{
  "permissions": [
    "fs:default",
    {
      "identifier": "fs:allow-exists",
      "allow": [{ "path": "$HOME" }, { "path": "$HOME/**/*" }]
    }
  ]
}
```

`allow` 和 `deny` 中可用的全部路径变量见下面的[作用域](#作用域)。
{{% /alert %}}

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    "fs:default",
    {
      "identifier": "fs:allow-exists",
      "allow": [{ "path": "$APPDATA/*" }]
    }
  ]
}
```

### 作用域

该插件的权限包含用于定义哪些路径被允许或明确拒绝的作用域。
关于作用域的更多信息，请参阅[命令作用域](../../security/3-scope/)。

每个 `allow` 或 `deny` 作用域都必须包含一个数组，列出应被允许或拒绝的所有路径。
作用域条目的格式为 `{ path: string }`。

{{% alert title="注意" %}}
`deny` 优先于 `allow`，因此如果某个路径被某个作用域拒绝，即使另一个作用域允许它，运行时也会被阻止。
{{% /alert %}}

作用域条目可以使用 `$<path>` 变量来引用常见系统路径，例如主目录、应用资源目录和配置目录。下表列出了你可以引用的所有常见路径：

| 路径                                                                        | 变量      |
| --------------------------------------------------------------------------- | ------------- |
| [appConfigDir](https://tauri.app/reference/javascript/api/namespacepath/#appconfigdir)       | $APPCONFIG    |
| [appDataDir](https://tauri.app/reference/javascript/api/namespacepath/#appdatadir)           | $APPDATA      |
| [appLocalDataDir](https://tauri.app/reference/javascript/api/namespacepath/#applocaldatadir) | $APPLOCALDATA |
| [appcacheDir](https://tauri.app/reference/javascript/api/namespacepath/#appcachedir)         | $APPCACHE     |
| [applogDir](https://tauri.app/reference/javascript/api/namespacepath/#applogdir)             | $APPLOG       |
| [audioDir](https://tauri.app/reference/javascript/api/namespacepath/#audiodir)               | $AUDIO        |
| [cacheDir](https://tauri.app/reference/javascript/api/namespacepath/#cachedir)               | $CACHE        |
| [configDir](https://tauri.app/reference/javascript/api/namespacepath/#configdir)             | $CONFIG       |
| [dataDir](https://tauri.app/reference/javascript/api/namespacepath/#datadir)                 | $DATA         |
| [localDataDir](https://tauri.app/reference/javascript/api/namespacepath/#localdatadir)       | $LOCALDATA    |
| [desktopDir](https://tauri.app/reference/javascript/api/namespacepath/#desktopdir)           | $DESKTOP      |
| [documentDir](https://tauri.app/reference/javascript/api/namespacepath/#documentdir)         | $DOCUMENT     |
| [downloadDir](https://tauri.app/reference/javascript/api/namespacepath/#downloaddir)         | $DOWNLOAD     |
| [executableDir](https://tauri.app/reference/javascript/api/namespacepath/#executabledir)     | $EXE          |
| [fontDir](https://tauri.app/reference/javascript/api/namespacepath/#fontdir)                 | $FONT         |
| [homeDir](https://tauri.app/reference/javascript/api/namespacepath/#homedir)                 | $HOME         |
| [pictureDir](https://tauri.app/reference/javascript/api/namespacepath/#picturedir)           | $PICTURE      |
| [publicDir](https://tauri.app/reference/javascript/api/namespacepath/#publicdir)             | $PUBLIC       |
| [runtimeDir](https://tauri.app/reference/javascript/api/namespacepath/#runtimedir)           | $RUNTIME      |
| [templateDir](https://tauri.app/reference/javascript/api/namespacepath/#templatedir)         | $TEMPLATE     |
| [videoDir](https://tauri.app/reference/javascript/api/namespacepath/#videodir)               | $VIDEO        |
| [resourceDir](https://tauri.app/reference/javascript/api/namespacepath/#resourcedir)         | $RESOURCE     |
| [tempDir](https://tauri.app/reference/javascript/api/namespacepath/#tempdir)                 | $TEMP         |

#### 示例

- 全局作用域

要把作用域应用到任何 `fs` 命令，请使用 `fs:scope` 权限：

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    {
      "identifier": "fs:scope",
      "allow": [{ "path": "$APPDATA" }, { "path": "$APPDATA/**/*" }]
    }
  ]
}
```

要把作用域应用到特定的 `fs` 命令，
请使用权限的对象形式 `{ "identifier": string, "allow"?: [], "deny"?: [] }`：

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    {
      "identifier": "fs:allow-rename",
      "allow": [{ "path": "$HOME/**/*" }]
    },
    {
      "identifier": "fs:allow-rename",
      "deny": [{ "path": "$HOME/.config/**/*" }]
    },
    {
      "identifier": "fs:allow-exists",
      "allow": [{ "path": "$APPDATA/*" }]
    }
  ]
}
```

在上面的示例中，你可以对 `$APPDATA` 下的任意子路径（不含子目录）使用 [`exists`](#是否存在) API，
以及使用 [`rename`](#重命名)。

{{% alert title="提示" %}}
如果你想在类 Unix 系统上访问点文件（如 `.gitignore`）或点目录（如 `.ssh`），
那么你需要指定完整路径 `/home/user/.ssh/example`，或在点目录路径组件之后使用 glob `/home/user/.ssh/*`。

如果在你的用例中这仍然不起作用，你可以配置插件把任意组件都当作合法的路径字面量。

```json
 "plugins": {
    "fs": {
      "requireLiteralLeadingDot": false
    }
  }
```

当你使用[对象形式](../../security/5-assetprotocol/)（而不是仅数组形式）时，**`app.security.assetProtocol.scope`** 也有同样的选项。涉及点目录的真实案例见 [tauri#13788](https://github.com/tauri-apps/tauri/issues/13788)。

{{% /alert %}}
