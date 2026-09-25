+++
title = "7 嵌入外部二进制文件"
date = 2026-09-25T21:31:08+08:00
weight = 7
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/sidecar/](https://tauri.app/develop/sidecar/)

你可能需要嵌入外部二进制文件来为应用添加额外功能，或者避免用户去安装额外依赖（例如 Node.js 或 Python）。我们把这类的二进制文件称为 `sidecar`。

二进制文件是用任何编程语言编写的可执行文件。常见用例是用 `pyinstaller` 打包的 Python CLI 应用或 API 服务器。

要打包你选定的二进制文件，你可以在 `tauri.conf.json` 的 `bundle` 对象中添加 `externalBin` 属性。
`externalBin` 配置期望一个字符串列表，使用绝对或相对路径指向二进制文件。

下面是一个说明 sidecar 配置的 Tauri 配置片段：

```json
{
  "bundle": {
    "externalBin": [
      "/absolute/path/to/sidecar",
      "../relative/path/to/binary",
      "binaries/my-sidecar"
    ]
  }
}
```

{{% alert title="注意" %}}

相对路径是相对于 `src-tauri` 目录中的 `tauri.conf.json` 文件而言的。
因此 `binaries/my-sidecar` 表示 `<PROJECT ROOT>/src-tauri/binaries/my-sidecar`。

{{% /alert %}}

要让外部二进制文件在每个受支持的架构上都能工作，指定路径上必须存在同名且带 `-$TARGET_TRIPLE` 后缀的二进制文件。
例如，`"externalBin": ["binaries/my-sidecar"]` 在 Linux 上需要 `src-tauri/binaries/my-sidecar-x86_64-unknown-linux-gnu` 可执行文件，在 Apple Silicon 的 macOS 上需要 `src-tauri/binaries/my-sidecar-aarch64-apple-darwin`。

你可以运行以下命令获取你**当前**平台的 `-$TARGET_TRIPLE` 后缀：

```sh
use tauri_plugin_shell::ShellExt;
use tauri_plugin_shell::process::CommandEvent;
use tauri::Emitter;

let sidecar_command = app.shell().sidecar("my-sidecar").unwrap();
let (mut rx, mut child) = sidecar_command
  .spawn()
  .expect("Failed to spawn sidecar");

tauri::async_runtime::spawn(async move {
  // read events such as stdout
  while let Some(event) = rx.recv().await {
    if let CommandEvent::Stdout(line_bytes) = event {
      let line = String::from_utf8_lossy(&line_bytes);
      app
        .emit("message", Some(format!("'{}'", line)))
        .expect("failed to emit event");
      // write to stdin
      child.write("message from Rust\n".as_bytes()).unwrap();
    }
  }
});
```

它会直接输出你主机的目标三元组（例如 `x86_64-unknown-linux-gnu` 或 `aarch64-apple-darwin`）。

{{% alert title="注意" %}}
`--print host-tuple` 标志是在 Rust 1.84.0 中加入的。如果你使用更早的版本，需要改为解析 `rustc -Vv` 的输出：

```sh
rustc -Vv | grep host | cut -f2 -d' '

# Windows PowerShell
rustc -Vv | Select-String "host:" | ForEach-Object {$_.Line.split(" ")[1]}
```

{{% /alert %}}

下面是一个把目标三元组追加到二进制文件名的 Node.js 脚本：

```javascript
import { execSync } from 'child_process';
import fs from 'fs';

const extension = process.platform === 'win32' ? '.exe' : '';

const targetTriple = execSync('rustc --print host-tuple').toString().trim();
if (!targetTriple) {
  console.error('Failed to determine platform target triple');
}
fs.renameSync(
  `src-tauri/binaries/sidecar${extension}`,
  `src-tauri/binaries/sidecar-${targetTriple}${extension}`
);
```

注意，如果你为与其运行架构不同的架构编译，这个脚本将无法工作，所以只能把它作为你自己构建脚本的起点。

## 从 Rust 运行

{{% alert title="注意" %}}
请先按照 [shell 插件指南](../../plugin/23-shell/)正确安装并初始化该插件。
如果插件未初始化并配置好，下面的示例无法工作。
{{% /alert %}}

在 Rust 侧，导入 `tauri_plugin_shell::ShellExt` trait，并在 AppHandle 上调用 `shell().sidecar()` 函数：

```rust
use tauri_plugin_shell::process::CommandEvent;
use tauri::Emitter;

let sidecar_command = app.shell().sidecar("my-sidecar").unwrap();
let (mut rx, mut child) = sidecar_command
  .spawn()
  .expect("Failed to spawn sidecar");

tauri::async_runtime::spawn(async move {
  // 读取 stdout 之类的事件
  while let Some(event) = rx.recv().await {
    if let CommandEvent::Stdout(line_bytes) = event {
      let line = String::from_utf8_lossy(&line_bytes);
      app
        .emit("message", Some(format!("'{}'", line)))
        .expect("failed to emit event");
      // 写入 stdin
      child.write("message from Rust\n".as_bytes()).unwrap();
    }
  }
});
```

{{% alert title="注意" %}}
`sidecar()` 函数只接受文件名，**不是**在 `externalBin` 数组中配置的完整路径。

给定如下配置：

```json
{
  "bundle": {
    "externalBin": ["binaries/app", "my-sidecar", "../scripts/sidecar"]
  }
}
```

执行该 sidecar 的正确方式是调用 `app.shell().sidecar(name)`，其中 `name` 是 `"app"`、`"my-sidecar"` 或 `"sidecar"`，
而不是 `"binaries/app"` 之类。
{{% /alert %}}

你可以把这段代码放进 Tauri 命令中以便轻松传递 AppHandle，也可以在 builder 脚本中保存对 AppHandle 的引用，以便在应用其它位置访问它。

## 从 JavaScript 运行

运行 sidecar 时，Tauri 要求你授予该 sidecar 在子进程上执行 `execute` 或 `spawn` 方法的权限。要授予该权限，请打开 `<PROJECT ROOT>/src-tauri/capabilities/default.json`，并把下面这段加入 permissions 数组。别忘了按前面提到的相对路径为你的 sidecar 命名。

```json
{
  "permissions": [
    "core:default",
    {
      "identifier": "shell:allow-execute",
      "allow": [
        {
          "name": "binaries/app",
          "sidecar": true
        }
      ]
    }
  ]
}
```

{{% alert title="注意" %}}

使用 `shell:allow-execute` 标识符是因为 sidecar 的子进程会通过 `command.execute()` 方法启动。要用 `command.spawn()` 运行它，你需要把标识符改为 `shell:allow-spawn`，或者按上面相同的结构向数组再添加一项，但标识符设为 `shell:allow-spawn`。

{{% /alert %}}

在 JavaScript 代码中，从 `@tauri-apps/plugin-shell` 模块导入 `Command` 类，并使用 `sidecar` 静态方法。

```javascript
import { Command } from '@tauri-apps/plugin-shell';
const command = Command.sidecar('binaries/my-sidecar');
const output = await command.execute();
```

{{% alert title="注意" %}}
传给 `Command.sidecar` 的字符串必须与 `externalBin` 配置数组中定义的某个字符串匹配。
{{% /alert %}}

## 传递参数

你可以像运行普通 [Command](https://doc.rust-lang.org/std/process/struct.Command.html) 那样向 Sidecar 命令传递参数。

参数既可以是**静态**的（例如 `-o` 或 `serve`），也可以是**动态**的（例如 `<file_path>` 或 `localhost:<PORT>`）。值为 `true` 将允许向该命令传递任意参数，`false` 则禁用所有参数。如果既没有设置 `true` 也没有设置 `false`，你就按实际调用顺序定义参数。静态参数按原样定义，动态参数可以用正则表达式定义。

首先，在 `src-tauri/capabilities/default.json` 中定义需要传给 sidecar 命令的参数：

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    {
      "identifier": "shell:allow-execute",
      "allow": [
        {
          "args": [
            "arg1",
            "-a",
            "--arg2",
            {
              "validator": "\\S+"
            }
          ],
          "name": "binaries/my-sidecar",
          "sidecar": true
        }
      ]
    }
  ]
}
```

{{% alert title="注意" %}}
如果你正在从 Tauri v1 迁移，Tauri v2 CLI 中的 `migrate` 命令应当会替你处理这一点。更多内容请阅读[自动迁移](../../quickstart/migrate/2-upgradefromtauri1/#自动迁移)。
{{% /alert %}}

然后，要调用该 sidecar 命令，只需把**所有**参数作为数组传入。

在 Rust 中：

```rust
#[tauri::command]
async fn call_my_sidecar(app: tauri::AppHandle) {
  let sidecar_command = app
    .shell()
    .sidecar("my-sidecar")
    .unwrap()
    .args(["arg1", "-a", "--arg2", "any-string-that-matches-the-validator"]);
  let (mut _rx, mut _child) = sidecar_command.spawn().unwrap();
}
```

在 JavaScript 中：

```javascript
import { Command } from '@tauri-apps/plugin-shell';
// 注意 args 数组与 `capabilities/default.json` 中指定的内容完全一致。
const command = Command.sidecar('binaries/my-sidecar', [
  'arg1',
  '-a',
  '--arg2',
  'any-string-that-matches-the-validator',
]);
const output = await command.execute();
```
