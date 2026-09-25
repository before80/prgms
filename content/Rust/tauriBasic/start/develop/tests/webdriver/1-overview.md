+++
title = "1 WebDriver 概述"
date = 2026-09-25T21:31:08+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/tests/webdriver/](https://tauri.app/develop/tests/webdriver/)

[WebDriver](https://www.w3.org/TR/webdriver/) 是一个与 Web 文档交互的标准化接口，主要用于自动化测试。与 Tauri 配合使用的推荐方式是 [WebdriverIO](https://webdriver.io/) 和 [`@wdio/tauri-service`](https://webdriver.io/docs/desktop-testing/tauri)，它可在 **Windows、Linux 和 macOS** 上工作。它由 WebdriverIO 项目维护，通过 `browser.tauri.execute()` 提供 Tauri API 访问、命令（IPC）模拟、前端与后端日志捕获以及 multiremote 支持。

默认情况下，该服务在你的应用内运行一个**内嵌的 WebDriver 服务器**，因此在任何平台上都不需要外部驱动——macOS 也是这样得到支持的。它也可以在 Windows 和 Linux 上通过 [`tauri-driver`](https://crates.io/crates/tauri-driver) 驱动平台的本地 WebDriver，或在所有平台上使用 [CrabNebula](https://crabnebula.dev) 的跨平台 `tauri-driver` 分支（在 macOS 上需要付费 API 密钥）。无论选择哪条路线，该服务都会检测你的应用二进制文件；在 `tauri-driver` 路线上，它还会在 Windows 上替你保持 Edge WebDriver 版本同步。

快速搭建项目的最快方式是 WebdriverIO 脚手架：

```shell
npm create wdio@latest ./
```

选择 **Desktop Testing**，并在框架提示处选择 **Tauri**。一个最小配置如下：

```typescript
export const config: WebdriverIO.Config = {
  services: [
    [
      'tauri',
      {
        appBinaryPath: './src-tauri/target/release/my-tauri-app',
        driverProvider: 'embedded',
      },
    ],
  ],
};
```

这套配置用到两个小型 Tauri 插件，是否使用取决于你的需求：

- **`tauri-plugin-wdio-webdriver`** 运行内嵌的 WebDriver 服务器。`embedded` 提供方（默认）需要它——服务通过它驱动你的应用，无需外部驱动，macOS 也是这样得到支持的。如果你想改用 `external` 或 `crabnebula` 提供方，可以跳过它。
- **`tauri-plugin-wdio`** 启用后端访问，包括：`browser.tauri.execute()`、命令（IPC）模拟以及日志捕获。

完整步骤请参阅 [插件设置](https://webdriver.io/docs/desktop-testing/tauri/plugin-setup)，如果使用 CrabNebula 提供方，请参阅 [CrabNebula 设置指南](https://webdriver.io/docs/desktop-testing/tauri/crabnebula-setup)。

对于快速的、只涉及渲染器的测试，还有一种 **browser 模式**：在普通 Chrome 中针对 Vite 开发服务器运行你的 Tauri 前端——不需要 Tauri 二进制、驱动或插件。它会拦截 `invoke()` 调用，让你用同样的 WDIO API 模拟命令并断言其参数。参见 [browser 模式指南](https://github.com/webdriverio/desktop-mobile/blob/main/packages/tauri-service/docs/browser-mode.md)。

关于 `@wdio/tauri-service` 的完整设置、配置与 API 参考，请查阅 [WebdriverIO Tauri 文档](https://webdriver.io/docs/desktop-testing/tauri)。

## 示例应用

使用该服务的完整可运行示例位于 [WebdriverIO desktop-mobile 仓库](https://github.com/webdriverio/desktop-mobile/tree/main/fixtures/e2e-apps/tauri)。

## 持续集成（CI）

WebDriver CI 指南说明了如何在 GitHub Actions 下运行这些测试，以及其背后的概念。

参见 [持续集成（CI）](../3-ci/)。

## 直接驱动 `tauri-driver`

如果你不使用 Node.js、更偏好 [Selenium](../example/1-selenium/)，或者要把 WebDriver 集成进自定义测试框架，你可以直接驱动 [`tauri-driver`](https://crates.io/crates/tauri-driver)，而不使用该服务。直接驱动时，桌面端只支持 Windows 和 Linux，因为 macOS 没有可用的 WKWebView 驱动工具（macOS 请使用服务的内嵌 WebDriver 服务器）。

参见[手动配置 WebDriver](../2-manualsetup/)：自行安装并驱动 tauri-driver（仅 Windows 和 Linux）。
