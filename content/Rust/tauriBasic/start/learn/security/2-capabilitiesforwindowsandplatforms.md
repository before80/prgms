+++
title = "2 针对不同窗口和平台的能力"
date = 2026-09-25T21:31:08+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/learn/security/capabilities-for-windows-and-platforms/](https://tauri.app/learn/security/capabilities-for-windows-and-platforms/)

本指南将帮助你自定义 Tauri 应用的能力（capabilities）。

## 本指南内容

- 在 Tauri 应用中创建多个窗口
- 为不同窗口使用不同的能力
- 使用平台特定的能力

## 前置条件

本练习应当在完成[《使用插件权限》](../1-usingpluginpermissions/)之后再阅读。

## 指南

### 1. 在 Tauri 应用中创建多个窗口

这里我们创建一个包含两个窗口的应用，标签分别为 `first` 和 `second`。
在 Tauri 应用中有多种创建窗口的方式。

#### 用 Tauri 配置文件创建窗口

在通常名为 `tauri.conf.json` 的 Tauri 配置文件中：

```javascript
  ...
  "app": {
    "windows": [
      {
        "label": "first",
        "title": "First",
        "width": 800,
        "height": 600
      },
      {
        "label": "second",
        "title": "Second",
        "width": 800,
        "height": 600
      }
    ],
  },
  ...
}
```

#### 以编程方式创建窗口

在创建 Tauri 应用的 Rust 代码中：

```rust
    .invoke_handler(tauri::generate_handler![greet])
    .setup(|app| {
        let webview_url = tauri::WebviewUrl::App("index.html".into());
        // 第一个窗口
        tauri::WebviewWindowBuilder::new(app, "first", webview_url.clone())
            .title("First")
            .build()?;
        // 第二个窗口
        tauri::WebviewWindowBuilder::new(app, "second", webview_url)
            .title("Second")
            .build()?;
        Ok(())
    })
    .run(context)
    .expect("error while running tauri application");
```

### 2. 为不同窗口应用不同的能力

Tauri 应用的各个窗口可以使用 Tauri 后端的不同功能或插件。
为了更好的安全性，建议只给每个窗口必要的能力。
我们模拟一个场景：`first` 窗口使用文件系统和对话框功能，而 `second` 只需要对话框功能。

#### 按类别拆分能力文件

建议按所启用操作的类别拆分能力文件。

`src-tauri/capabilities` 中的 JSON 文件会被能力系统纳入考虑。
这里我们把与文件系统和对话框相关的能力分别拆到 `filesystem.json` 和 `dialog.json`。

*Tauri 项目的文件树：*
```
/src
/src-tauri
  /capabilities
    filesystem.json
    dialog.json
  tauri.conf.json
package.json
README.md
```

#### 给 `first` 窗口文件系统能力

我们给 `first` 窗口读取 `$HOME` 目录内容的权限。

在能力文件中使用 `windows` 字段，填入一个或多个窗口标签。

```json
{
  "identifier": "fs-read-home",
  "description": "Allow access file access to home directory",
  "local": true,
  "windows": ["first"],
  "permissions": [
    "fs:allow-home-read",
  ]
}
```

#### 给 `first` 和 `second` 窗口对话框能力

我们给 `first` 和 `second` 窗口创建 “Yes/No” 对话框的权限。

在能力文件中使用 `windows` 字段，填入一个或多个窗口标签。

```json
{
  "identifier": "dialog",
  "description": "Allow to open a dialog",
  "local": true,
  "windows": ["first", "second"],
  "permissions": ["dialog:allow-ask"]
}
```

### 3. 让能力依赖平台

现在我们想让能力只在特定平台上生效。
我们让文件系统能力只在 `linux` 和 `windows` 上生效。

在能力文件中使用 `platforms` 字段使它成为平台特定的。

```json
{
  "identifier": "fs-read-home",
  "description": "Allow access file access to home directory",
  "local": true,
  "windows": ["first"],
  "permissions": [
    "fs:allow-home-read",
  ],
  "platforms": ["linux", "windows"]
}
```

当前可用的平台有 `linux`、`windows`、`macos`、`android` 和 `ios`。

## 结论与资源

我们学习了如何在 Tauri 应用中创建多个窗口，并为它们指定特定的能力。此外，这些能力还可以只针对某些平台生效。

一个使用窗口能力的示例应用可以在 [Tauri GitHub 仓库](https://github.com/tauri-apps/tauri)的 [`api` 示例](https://github.com/tauri-apps/tauri/tree/dev/examples/api)中找到。
能力文件中可用的字段列在[能力](https://tauri.app/reference/acl/capability/)参考中。
