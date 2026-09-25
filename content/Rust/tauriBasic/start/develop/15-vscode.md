+++
title = "5 在 VS Code 中调试"
date = 2026-09-25T21:31:08+08:00
weight = 15
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/debug/vscode/](https://tauri.app/develop/debug/vscode/)

本指南将带你配置 VS Code，用于调试 [Tauri 应用的核心进程](../../concept/3-processmodel/#核心进程)。

## 使用 vscode-lldb 扩展的所有平台

### 前置条件

安装 [`vscode-lldb`](https://marketplace.visualstudio.com/items?itemName=vadimcn.vscode-lldb) 扩展。

### 配置 launch.json

创建 `.vscode/launch.json` 文件，并把下面的 JSON 内容粘贴进去：

```json
{
  // 使用 IntelliSense 了解可能的属性。
  // 悬停可查看现有属性的说明。
  // 更多信息请访问：https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "type": "lldb",
      "request": "launch",
      "name": "Tauri Development Debug",
      "cargo": {
        "args": [
          "build",
          "--manifest-path=./src-tauri/Cargo.toml",
          "--no-default-features"
        ]
      },
      // 如果使用了 `beforeDevCommand`，其任务必须在 `.vscode/tasks.json` 中配置
      "preLaunchTask": "ui:dev"
    },
    {
      "type": "lldb",
      "request": "launch",
      "name": "Tauri Production Debug",
      "cargo": {
        "args": ["build", "--release", "--manifest-path=./src-tauri/Cargo.toml"]
      },
      // 如果使用了 `beforeBuildCommand`，其任务必须在 `.vscode/tasks.json` 中配置
      "preLaunchTask": "ui:build"
    }
  ]
}
```

它直接使用 `cargo` 构建 Rust 应用，并在开发模式和生产模式下加载它。

注意它不使用 Tauri CLI，因此 CLI 专有的特性不会被执行。`beforeDevCommand` 和 `beforeBuildCommand` 脚本必须事先执行，或者在 `preLaunchTask` 字段中配置为任务。下面是一个 `.vscode/tasks.json` 示例，其中有两个任务：一个用于 `beforeDevCommand`（启动开发服务器），一个用于 `beforeBuildCommand`：

```json
{
  // 关于 tasks.json 格式的文档见 https://go.microsoft.com/fwlink/?LinkId=733558
  "version": "2.0.0",
  "tasks": [
    {
      "label": "ui:dev",
      "type": "shell",
      // `dev` 会在后台持续运行
      // 理想情况下你还应配置 `problemMatcher`
      // 见 https://code.visualstudio.com/docs/editor/tasks#_can-a-background-task-be-used-as-a-prelaunchtask-in-launchjson
      "isBackground": true,
      // 改成你的 `beforeDevCommand`：
      "command": "yarn",
      "args": ["dev"]
    },
    {
      "label": "ui:build",
      "type": "shell",
      // 改成你的 `beforeBuildCommand`：
      "command": "yarn",
      "args": ["build"]
    }
  ]
}
```

现在你可以在 `src-tauri/src/main.rs` 或任何其它 Rust 文件中设置断点，然后按 `F5` 开始调试。

## 在 Windows 上使用 Visual Studio Windows Debugger

Visual Studio Windows Debugger 是仅限 Windows 的调试器，通常比 [`vscode-lldb`](https://marketplace.visualstudio.com/items?itemName=vadimcn.vscode-lldb) 更快，并且对某些 Rust 特性（例如枚举）有更好的支持。

### 前置条件

安装 [C/C++](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools) 扩展，并按照 https://code.visualstudio.com/docs/cpp/config-msvc#_prerequisites 安装 Visual Studio Windows Debugger。

### 配置 launch.json 和 tasks.json

```json
{
  // 使用 IntelliSense 了解可能的属性。
  // 悬停可查看现有属性的说明。
  // 更多信息请访问：https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Launch App Debug",
      "type": "cppvsdbg",
      "request": "launch",
      // 把 exe 名称改为你实际的 exe 名称
      //（要调试 release 构建，请把 `target/debug` 改为 `release/debug`）
      "program": "${workspaceRoot}/src-tauri/target/debug/your-app-name-here.exe",
      "cwd": "${workspaceRoot}",
      "preLaunchTask": "ui:dev"
    }
  ]
}
```

注意它不使用 Tauri CLI，因此 CLI 专有的特性不会被执行。`tasks.json` 与 `lldb` 的情况相同，只是如果你想让它每次启动前都编译，就需要添加一个配置组，并让 `launch.json` 中的 `preLaunchTask` 指向它。

下面是一个把开发服务器（等价于 `beforeDevCommand`）与编译（`cargo build`）作为一个组运行的示例。要使用它，请把 `launch.json` 中的 `preLaunchTask` 配置改为 `dev`（或你为该组起的任何名字）。

```json
{
  // 关于 tasks.json 格式的文档见 https://go.microsoft.com/fwlink/?LinkId=733558
  "version": "2.0.0",
  "tasks": [
    {
      "label": "build:debug",
      "type": "cargo",
      "command": "build",
      "options": {
        "cwd": "${workspaceRoot}/src-tauri"
      }
    },
    {
      "label": "ui:dev",
      "type": "shell",
      // `dev` 会在后台持续运行
      // 理想情况下你还应配置 `problemMatcher`
      // 见 https://code.visualstudio.com/docs/editor/tasks#_can-a-background-task-be-used-as-a-prelaunchtask-in-launchjson
      "isBackground": true,
      // 改成你的 `beforeDevCommand`：
      "command": "yarn",
      "args": ["dev"]
    },
    {
      "label": "dev",
      "dependsOn": ["build:debug", "ui:dev"],
      "group": {
        "kind": "build"
      }
    }
  ]
}
```
