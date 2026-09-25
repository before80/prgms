+++
title = "2 把 Node.js 用作 Sidecar"
date = 2026-09-25T21:31:08+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/learn/sidecar-nodejs/](https://tauri.app/learn/sidecar-nodejs/)

在本指南中，我们将把一个 Node.js 应用打包成自包含的二进制文件，作为 Tauri 应用中的 sidecar 使用，而无需终端用户安装 Node.js。
本示例教程只适用于桌面操作系统。

为了更深入地理解 Tauri sidecar 的工作方式，我们建议先阅读通用的 [sidecar 指南](../../develop/7-sidecar/)。

## 目标

- 把一个 Node.js 应用打包成二进制文件。
- 把这个二进制文件集成为 Tauri sidecar。

## 实现细节

- 为此我们使用 [pkg](https://github.com/yao-pkg/pkg) 工具，但任何能把 JavaScript 或 TypeScript 编译成二进制应用的工具都可以。
- 你也可以把 Node 运行时本身嵌入 Tauri 应用，并以资源的形式附带打包后的 JavaScript，但这样会以可读性较高的文件形式附带 JavaScript 内容，而且运行时通常比用 `pkg` 打包的应用更大。

在这个示例中，我们将创建一个 Node.js 应用，它从命令行 [process.argv](https://nodejs.org/docs/latest/api/process.html#processargv) 读取输入，并用 [console.log](https://nodejs.org/api/console.html#consolelogdata-args) 把输出写到 stdout。<br/>
你也可以利用其它进程间通信方式，例如 localhost 服务器、stdin/stdout 或本地 socket。
注意它们各有自己的优点、缺点和安全考量。

## 前置条件

一个已经配置好 shell 插件、能在本地编译并运行的 Tauri 应用。

{{% alert title="创建一个实验应用" %}}

如果你不是高级用户，**强烈建议**你使用这里给出的选项和框架。它只是一个实验，做完之后你可以把项目删掉。

- 项目名：`node-sidecar-lab`
- 选择前端使用哪种语言：`Typescript / Javascript`
- 选择包管理器：`pnpm`
- 选择 UI 模板：`Vanilla`
- 选择 UI 风格：`Typescript`

{{% /alert %}}

{{% alert title="注意" %}}
请先按照 [shell 插件指南](../../plugin/23-shell/)正确安装并初始化该插件。
如果插件未初始化并配置好，下面的示例无法工作。
{{% /alert %}}

## 指南

### 1. 初始化 Sidecar 项目

让我们创建一个新的 Node.js 项目来存放 sidecar 实现。
**在你的 Tauri 应用根文件夹中**创建一个新目录（本示例中我们叫它 `sidecar-app`），并在该目录中运行你所偏好的 Node.js 包管理器的 `init` 命令：

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm init
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn init
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm init
```

{{% /tab %}}

{{< /tabpane >}}
我们将用 [pkg](https://github.com/yao-pkg/pkg) 等方案把 Node.js 应用编译成自包含的二进制文件。
先把它作为开发依赖安装到新建的 `sidecar-app` 中：

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm add @yao-pkg/pkg --save-dev
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn add @yao-pkg/pkg --dev
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm add @yao-pkg/pkg --save-dev
```

{{% /tab %}}

{{< /tabpane >}}
### 2. 编写 Sidecar 逻辑

现在我们可以开始编写将由 Tauri 应用执行的 JavaScript 代码了。

在这个示例中，我们会处理来自命令行参数的一个命令并把输出写到 stdout，
这意味着我们的进程是短生命周期的，一次只处理一个命令。
如果你的应用必须长期运行，请考虑使用其它进程间通信方式。

让我们在 `sidecar-app` 目录中创建 `index.js` 文件，写一个基础的 Node.js 应用：

```js

switch (command) {
  case 'hello':
    const message = process.argv[3];
    console.log(`Hello ${message}!`);
    break;
  default:
    console.error(`unknown command ${command}`);
    process.exit(1);
}
```

### 3. 打包 Sidecar

要把 Node.js 应用打包成自包含的二进制文件，请在 `package.json` 中创建一个脚本：

```json
{
  "scripts": {
    "build": "pkg index.ts --output my-sidecar"
  }
}
```

**包管理器**

{{< tabpane text=true persist=disabled >}}
{{% tab header="npm" %}}

```sh
npm run build
```

{{% /tab %}}

{{% tab header="yarn" %}}

```sh
yarn build
```

{{% /tab %}}

{{% tab header="pnpm" %}}

```sh
pnpm build
```

{{% /tab %}}

{{< /tabpane >}}
这会在 Linux 和 macOS 上生成 `sidecar-app/my-sidecar` 二进制文件，在 Windows 上生成 `sidecar-app/my-sidecar.exe` 可执行文件。

对于 sidecar 应用，我们需要确保二进制文件按正确的模式命名，更多信息请阅读[嵌入外部二进制文件](../../develop/7-sidecar/)。
要把这个文件重命名为 Tauri 期望的 sidecar 文件名并移动到我们的 Tauri 项目中，可以把下面的 Node.js 脚本作为起点：

```js
import { execSync } from 'child_process';
import fs from 'fs';

const ext = process.platform === 'win32' ? '.exe' : '';

const targetTriple = execSync('rustc --print host-tuple').toString().trim();
if (!targetTriple) {
  console.error('Failed to determine platform target triple');
}
// TODO：创建 `src-tauri/binaries` 目录
fs.renameSync(
  `my-sidecar${ext}`,
  `../src-tauri/binaries/my-sidecar-${targetTriple}${ext}`
);
```

{{% alert title="注意" %}}
`--print host-tuple` 标志是在 Rust 1.84.0 中加入的。如果你使用更早的版本，需要改为解析 `rustc -Vv` 的输出：

```js
const targetTriple = /host: (\S+)/g.exec(rustInfo)[1];
```

{{% /alert %}}

然后在 `sidecar-app` 目录中运行 `node rename.js`。

到这一步，`/src-tauri/binaries` 目录中应当包含重命名后的 sidecar 二进制文件。

### 4. 设置 plugin-shell 权限

安装 [shell 插件](../../plugin/23-shell/)之后，请确保配置好所需的能力。

注意我们使用了 `"args": true`，但你也可以选择提供一个数组 `["hello"]`，[更多内容见此](../../develop/7-sidecar/#传递参数)。

```json
{
  "permissions": [
    "core:default",
    "opener:default",
    {
      "identifier": "shell:allow-execute",
      "allow": [
        {
          "args": true,
          "name": "binaries/my-sidecar",
          "sidecar": true
        }
      ]
    }
  ]
}
```

### 5. 在 Tauri 应用中配置 Sidecar

现在 Node.js 应用已经准备好了，我们可以通过配置 [`bundle > externalBin`](https://tauri.app/reference/config/#externalbin) 数组把它接到 Tauri 应用上：

```json
{
  "bundle": {
    "externalBin": ["binaries/my-sidecar"]
  }
}
```

只要 sidecar 二进制文件以 `src-tauri/binaries/my-sidecar-<target-triple>` 的形式存在，Tauri CLI 就会负责它的打包。

### 6. 执行 Sidecar

我们既可以从 Rust 代码运行 sidecar 二进制文件，也可以直接从 JavaScript 运行。

**语言**

{{< tabpane text=true persist=disabled >}}
{{% tab header="JavaScript" %}}

让我们直接在 Node.js sidecar 中执行 `hello` 命令：

```js
import { Command } from '@tauri-apps/plugin-shell';

const message = 'Tauri';

const command = Command.sidecar('binaries/my-sidecar', ['hello', message]);
const output = await command.execute();
// 一切配置正确后，浏览器控制台应当打印 "Hello Tauri"。
console.log(output.stdout)
```

{{% /tab %}}

{{% tab header="Rust" %}}

让我们把一个 `hello` Tauri 命令管道接到 Node.js sidecar 上：

```rust

#[tauri::command]
async fn hello(app: tauri::AppHandle, cmd: String, message: String) -> String {
    let sidecar_command = app
        .shell()
        .sidecar("my-sidecar")
        .unwrap()
        .arg(cmd)
        .arg(message);
    let output = sidecar_command.output().await.unwrap();
    String::from_utf8(output.stdout).unwrap()
}
```

在 `invoke_handler` 中注册它，并在前端这样调用：

```js
import { invoke } from "@tauri-apps/api/core";

const message = "Tauri"
console.log(await invoke("hello", { cmd: 'hello', message }))

```

{{% /tab %}}

{{< /tabpane >}}
### 7. 运行

让我们测试一下。

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
用 F12（macOS 上是 `Cmd+Option+I`）打开 DevTools，你应该能看到 sidecar 命令的输出。

如果你遇到任何问题，请在 [GitHub](https://github.com/tauri-apps/tauri-docs) 上提 issue。
