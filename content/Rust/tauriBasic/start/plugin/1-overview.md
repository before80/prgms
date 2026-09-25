+++
title = "1 功能与示例"
date = 2026-09-25T21:31:08+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/plugin/](https://tauri.app/plugin/)

Tauri 在设计时就考虑了可扩展性。在本页中你会发现：

- **官方功能**：Tauri 内置的特性与功能
- **社区资源**：由 Tauri 社区构建的更多插件与示例。你也可以在 [Awesome Tauri](https://github.com/tauri-apps/awesome-tauri) 上贡献自己的作品
- **支持表**：显示每个官方插件支持哪些平台的兼容性表格

**使用搜索与筛选功能查找功能或社区资源：**

#### 官方功能

- [Autostart](../2-autostart/)：在系统启动时自动运行你的应用
- [Barcode Scanner](../3-barcodescanner/)：扫描条形码与二维码
- [Biometric](../4-biometric/)：使用系统生物识别进行认证
- [CLI](../5-cli/)：把你的应用解析为命令行界面
- [Clipboard](../6-clipboard/)：读写系统剪贴板
- [Deep Linking](../7-deeplinking/)：把你的应用注册为 URL 的处理程序
- [Dialog](../8-dialog/)：原生系统对话框
- [File System](../9-filesystem/)：读写文件与目录
- [Geolocation](../10-geolocation/)：获取设备位置
- [Global Shortcut](../11-globalshortcut/)：注册全局快捷键
- [Haptics](../12-haptics/)：触发设备触觉反馈
- [HTTP Client](../13-httpclient/)：用 Rust 发起 HTTP 请求
- [Localhost](../14-localhost/)：在生产应用中运行 localhost 服务器
- [Logging](../15-logging/)：把日志写到控制台、文件或 Webview
- [NFC](../16-nfc/)：读写 NFC 标签
- [Notifications](../17-notification/)：发送系统通知
- [Opener](../18-opener/)：用默认应用打开文件或 URL
- [OS Information](../19-osinfo/)：读取操作系统信息
- [Persisted Scope](../20-persistedscope/)：在多次运行之间持久化运行时作用域
- [Positioner](../21-positioner/)：把窗口移动到指定位置
- [Process](../22-process/)：访问当前进程
- [Shell](../23-shell/)：访问系统 shell
- [Single Instance](../24-singleinstance/)：确保应用只运行一个实例
- [SQL](../25-sql/)：使用 SQL 数据库
- [Store](../26-store/)：持久化键值存储
- [Stronghold](../27-stronghold/)：加密的安全存储
- [Updater](../28-updater/)：为你的应用提供更新
- [Upload](../29-upload/)：通过 HTTP 上传文件
- [Websocket](../30-websocket/)：使用 WebSocket 连接
- [Window State](../31-windowstate/)：保存与恢复窗口状态

#### 社区插件

社区贡献的插件列表请见 [Awesome Tauri](https://github.com/tauri-apps/awesome-tauri)。

#### 社区集成

社区贡献的集成列表请见 [Awesome Tauri](https://github.com/tauri-apps/awesome-tauri)。

## 支持表

将鼠标悬停在 “\*” 上可查看说明。更多细节请访问各插件页面。

| 插件 | Windows | Linux | macOS | Android | iOS |
| --- | --- | --- | --- | --- | --- |
| [Autostart](../2-autostart/) | 完整 | 完整 | 完整 | 不支持 | 不支持 |
| [Barcode Scanner](../3-barcodescanner/) | 不支持 | 不支持 | 不支持 | 完整 | 完整 |
| [Biometric](../4-biometric/) | 不支持 | 不支持 | 不支持 | 完整 | 完整 |
| [CLI](../5-cli/) | 完整 | 完整 | 完整 | 不支持 | 不支持 |
| [Clipboard](../6-clipboard/) | 完整 | 完整 | 完整 | 部分 | 部分 |
| [Deep Linking](../7-deeplinking/) | 完整 | 完整 | 部分 | 部分 | 部分 |
| [Dialog](../8-dialog/) | 完整 | 完整 | 完整 | 部分 | 部分 |
| [File System](../9-filesystem/) | 完整 | 完整 | 完整 | 部分 | 部分 |
| [Geolocation](../10-geolocation/) | 不支持 | 不支持 | 不支持 | 完整 | 完整 |
| [Global Shortcut](../11-globalshortcut/) | 完整 | 完整 | 完整 | 不支持 | 不支持 |
| [Haptics](../12-haptics/) | 不支持 | 不支持 | 不支持 | 完整 | 完整 |
| [HTTP Client](../13-httpclient/) | 完整 | 完整 | 完整 | 完整 | 完整 |
| [Localhost](../14-localhost/) | 完整 | 完整 | 完整 | 不支持 | 不支持 |
| [Logging](../15-logging/) | 完整 | 完整 | 完整 | 完整 | 完整 |
| [NFC](../16-nfc/) | 不支持 | 不支持 | 不支持 | 完整 | 完整 |
| [Notifications](../17-notification/) | 完整 | 完整 | 完整 | 完整 | 完整 |
| [Opener](../18-opener/) | 完整 | 完整 | 完整 | 部分 | 部分 |
| [OS Information](../19-osinfo/) | 完整 | 完整 | 完整 | 完整 | 完整 |
| [Persisted Scope](../20-persistedscope/) | 完整 | 完整 | 完整 | 完整 | 完整 |
| [Positioner](../21-positioner/) | 完整 | 完整 | 完整 | 不支持 | 不支持 |
| [Process](../22-process/) | 完整 | 完整 | 完整 | 不支持 | 不支持 |
| [Shell](../23-shell/) | 完整 | 完整 | 完整 | 部分 | 部分 |
| [Single Instance](../24-singleinstance/) | 完整 | 完整 | 完整 | 不支持 | 不支持 |
| [SQL](../25-sql/) | 完整 | 完整 | 完整 | 完整 | 完整 |
| [Store](../26-store/) | 完整 | 完整 | 完整 | 完整 | 完整 |
| [Stronghold](../27-stronghold/) | 完整 | 完整 | 完整 | 完整 | 完整 |
| [Updater](../28-updater/) | 完整 | 完整 | 完整 | 不支持 | 不支持 |
| [Upload](../29-upload/) | 完整 | 完整 | 完整 | 完整 | 完整 |
| [Websocket](../30-websocket/) | 完整 | 完整 | 完整 | 完整 | 完整 |
| [Window State](../31-windowstate/) | 完整 | 完整 | 完整 | 不支持 | 不支持 |
