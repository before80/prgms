+++
title = "2 手动配置"
date = 2026-09-25T21:31:08+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/tests/webdriver/manual-setup/](https://tauri.app/develop/tests/webdriver/manual-setup/)

本页介绍如何直接驱动 [`tauri-driver`](https://crates.io/crates/tauri-driver)，而不使用 [`@wdio/tauri-service`](https://webdriver.io/docs/desktop-testing/tauri)。如果你不使用 Node.js、更偏好 [Selenium](../example/1-selenium/)，或者要把 WebDriver 集成进自定义测试框架，请选用这条路线。对大多数项目来说，使用该服务是更简单的路径——它把下面的一切都自动化了，并且还支持 macOS。要开始使用它，请参阅 [WebDriver 概述](../1-overview/)。

直接驱动 `tauri-driver` 时，桌面端只支持 Windows 和 Linux，因为 macOS 没有可用的 WKWebView 驱动工具。iOS 和 Android 可以通过 Appium 2 工作，但目前流程还不够顺畅。

## 系统依赖

安装最新的 [`tauri-driver`](https://crates.io/crates/tauri-driver)，或通过以下命令更新已有安装：

```shell
cargo install tauri-driver --locked
```

由于我们目前使用平台原生的 [WebDriver](https://www.w3.org/TR/webdriver/) 服务器，在受支持的平台上运行 [`tauri-driver`](https://crates.io/crates/tauri-driver) 有一些要求。

### Linux

在 Linux 平台上我们使用 `WebKitWebDriver`。先运行 `which WebKitWebDriver` 命令检查该二进制文件是否已存在，因为有些发行版把它打包在常规 WebKit 包中。其它平台可能有单独的包，例如 Debian 系发行版上的 `webkit2gtk-driver`。

### Windows

请务必获取与你的应用构建和测试所在的 Windows Edge 版本相匹配的 [Microsoft Edge Driver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) 版本。在保持更新的 Windows 安装上，这几乎总是最新的稳定版。如果两个版本不匹配，你的 WebDriver 测试套件可能会在尝试连接时挂起。

你可以使用 [msedgedriver-tool](https://github.com/chippers/msedgedriver-tool) 下载合适的 Microsoft Edge Driver：

```powershell
& "$HOME/.cargo/bin/msedgedriver-tool.exe"
```

下载内容包含一个名为 `msedgedriver.exe` 的二进制文件。[`tauri-driver`](https://crates.io/crates/tauri-driver) 会在 `$PATH` 中查找该二进制文件，因此请确保它位于路径中，或者对 [`tauri-driver`](https://crates.io/crates/tauri-driver) 使用 `--native-driver` 选项。你可能想把它作为 CI 配置流程的一部分自动下载，以确保 Windows CI 机器上的 Edge 和 Edge Driver 版本保持同步。具体做法的指南可能会在以后补充。

## 示例应用

下面是分步指南，展示如何创建一个用 WebDriver 测试的最小示例应用。

如果你想直接看指南的结果，浏览一个使用它的完整最小代码库，可以访问 https://github.com/tauri-apps/webdriver-example。

- [Selenium](../example/1-selenium/)
- [WebdriverIO](../example/2-webdriverio/)

## 持续集成（CI）

上面的示例也附带了一个用 GitHub Actions 测试的 CI 脚本，但你可能仍会对下面的 WebDriver CI 指南感兴趣，因为它更详细地解释了相关概念。

参见 [持续集成（CI）](../3-ci/)。
