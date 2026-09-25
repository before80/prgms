+++
title = "1 测试概述"
date = 2026-09-25T21:31:08+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

> 原文链接: [https://tauri.app/develop/tests/](https://tauri.app/develop/tests/)

Tauri 通过 mock 运行时支持单元测试和集成测试。在 mock 运行时下，不会执行原生 webview 库。[关于 mock 运行时的更多内容见此](../2-mocking/)。

Tauri 还通过 WebDriver 协议支持端到端测试。[WebdriverIO 的 Tauri 测试](https://webdriver.io/docs/desktop-testing/tauri)
支持 Windows、Linux 和 macOS；由于 macOS 没有提供桌面端 WebDriver 客户端，WebDriver 协议也可以在 Windows 和 Linux 上直接驱动。[关于 WebDriver 支持的更多内容见此](../webdriver/1-overview/)。

我们提供 [tauri-action](https://github.com/tauri-apps/tauri-action) 来帮助运行 GitHub Actions，但只要每个平台都安装了编译所需的库，任何 CI/CD 运行器都可以与 Tauri 配合使用。
