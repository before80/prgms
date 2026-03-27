+++
title = "第35章 跨平台桌面开发"
weight = 350
date = "2026-03-25T12:56:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# Chapter-35 - 跨平台桌面开发

## 35.1 Electron

### 35.1.1 Electron 架构：主进程 + 渲染进程

Electron 使用 Chromium + Node.js，分为：
- **主进程（Main Process）**：Node.js 环境，管理窗口、系统操作
- **渲染进程（Renderer Process）**：Chromium 环境，运行 React 应用

### 35.1.2 React + Electron 项目搭建

```bash
# npm create electron-vite@latest：调用 npm 执行 electron-vite 脚手架工具
# my-app：项目名称（会创建一个同名文件夹）
# electron-vite 集成了 Vite + Electron，比纯 Electron 配置少很多
npm create electron-vite@latest my-app
```

### 35.1.3 IPC 通信：主进程与渲染进程数据交换

```javascript
// 主进程（main/index.ts）
import { app, ipcMain } from 'electron'

ipcMain.handle('get-app-version', () => {
  return app.getVersion()
})

ipcMain.handle('open-file-dialog', async () => {
  const { dialog } = require('electron')
  const result = await dialog.showOpenDialog({ properties: ['openFile'] })
  return result.filePaths
})
```

```javascript
// 渲染进程（ preload.cjs，用于安全暴露 API）
const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),
  openFileDialog: () => ipcRenderer.invoke('open-file-dialog')
})
```

```javascript
// React 组件中调用
const version = await window.electronAPI.getAppVersion()
```

### 35.1.4 electron-builder 打包发布

```bash
npm install -D electron-builder
```

```json
// electron-builder.json
{
  // 应用唯一标识符，格式通常为 com.公司名.产品名，用于系统安装和卸载
  "appId": "com.myapp.desktop",
  // 打包后显示的应用名称（即开始菜单/程序列表中的名字）
  "productName": "MyApp",
  // 打包输出目录，"release" 文件夹下会生成各平台的安装包
  "directories": { "output": "release" },
  // 需要打包进应用的文件或目录（** 通配符表示递归匹配）
  // 此处将 Vite 构建产物 dist 目录下的所有文件打包
  "files": ["dist/**/*"],
  // Windows 平台打包配置
  // target 指定打包格式：nsis = 安装向导格式（.exe），portable = 单文件便携版
  // 可选值还有：portable、appx、msi 等
  "win": { "target": ["nsis"] },
  // macOS 平台打包配置
  // target 可选：dmg（磁盘镜像）、pkg（安装包）、zip（压缩包）
  "mac": { "target": ["dmg"] },
  // Linux 平台打包配置
  // target 可选：AppImage（通用可执行格式）、deb（Debian/Ubuntu）、rpm（Fedora/RHEL）、tar.gz
  "linux": { "target": ["AppImage"] }
}
```

---

## 35.2 Tauri

### 35.2.1 Tauri 的优势：体积小、安全、Rust 后端

Tauri 用 Rust 替代 Node.js 作为后端，产物极小（~3MB vs Electron 的 100MB+）。包体积小的代价是：Node.js 生态不可用，系统级 API 需要额外配置。

### 35.2.2 React + Tauri 项目搭建

```bash
# npm create tauri-app@latest：调用 npm 执行 tauri-app 脚手架工具
# my-app：项目名称
# -- --template react-ts：两个 -- 的含义：
#   第一个 --：npm create 的标准分隔符，告诉 npm 后面是给 tauri-app 的参数
#   第二个 --：tauri-app 的参数分隔符
#   template react-ts：指定使用 React + TypeScript 模板
npm create tauri-app@latest my-app -- --template react-ts
cd my-app
npm run tauri dev
```

### 35.2.3 Tauri 命令调用

```rust
// src-tauri/src/lib.rs
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {} from Rust! 🦀", name)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("启动 Tauri 出错了");
}
```

```javascript
// React 组件中调用
import { invoke } from '@tauri-apps/api/tauri'

const greeting = await invoke('greet', { name: 'World' })
console.log(greeting) // "Hello, World from Rust! 🦀"
```

### 35.2.4 Tauri 权限配置（Tauri 2.x 新增）

Tauri 2.x 引入了权限系统，访问系统 API 需要声明权限：

```json
// src-tauri/capabilities/default.json
{
  "identifier": "default",           // 权限配置的唯一名称，"default" 表示这是默认权限集
  "description": "默认权限",          // 描述，供开发者和 Tauri 工具链使用，不影响实际行为
  "windows": ["main"],               // 该权限适用的窗口名称（与 src-tauri-tauri.conf.json 中窗口配置对应）
  "permissions": [                   // Tauri 2.x 权限白名单，必须显式声明才能调用对应系统 API
    "core:default",                   // 核心 API（窗口管理、应用信息等基础能力）
    "dialog:default",                // 对话框 API（打开/保存文件、弹出提示框等）
    "fs:default",                     // 文件系统 API（默认已包含常见目录的读写权限，可满足大多数场景）
    "shell:default"                   // Shell API（打开外部链接、启动系统应用等）
  ]
}
```

---

## 35.3 Tauri vs Electron

### 35.3.1 体积与性能对比

| 对比 | Electron | Tauri |
|------|---------|--------|
| 产物大小 | ~100MB+ | ~3-10MB |
| 启动速度 | 慢（Chromium 启动开销大） | 快 |
| 内存占用 | 高 | 低 |
| Node.js 生态 | ✅ 完全支持 | ❌ 不可用 |
| 系统 API | 通过 Node 模块 | 需 Rust 插件或权限配置 |
| 社区成熟度 | 非常成熟（2013年起） | 较新（Tauri 2.0 于 2024 年） |

### 35.3.2 安全性对比

- **Electron**：Node.js 完全可用，安全风险较高，需手动沙箱化
- **Tauri**：默认禁用 Node.js，通过权限系统白名单访问系统资源，更安全

### 35.3.3 选型建议

- 需要小体积、高安全、快速启动 → **Tauri**（推荐新项目）
- 需要复杂 Node.js 生态、Native 模块支持 → **Electron**
- 已经在用 Electron 的老项目 → 没必要迁移，Tauri 的学习曲线也值得考虑

---

## 本章小结

本章我们学习了 React 的跨平台桌面开发：

- **Electron**：成熟稳定，Node.js 生态丰富，包体积约 100MB+
- **Tauri**：轻量安全，Rust 后端，包体积仅 3-10MB
- **IPC 通信**：Electron 用 `ipcMain`/`ipcRenderer`，Tauri 用 `invoke()`
- **Tauri 2.x**：新增权限系统，系统 API 访问需声明权限

选 Electron 还是 Tauri？一句话：**新项目优先 Tauri，老项目别折腾迁移**。下一章我们将学习 **React 工程化与架构**！🏗️