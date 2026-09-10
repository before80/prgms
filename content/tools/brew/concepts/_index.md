+++
title = "3 核心概念"
date = 2026-09-09T13:39:44+08:00
weight = 30
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://brew.sh/](https://brew.sh/)

要真正“掌握” brew，而不是只会复制几条命令，就需要理解它背后的设计约束：为什么必须装在默认前缀、为什么拒绝 sudo、为什么有些包叫 keg-only、第三方 tap 为什么需要信任。本章把这些概念逐一讲透。

本章内容：

- [3.1 默认前缀、bottle 与下载缓存](3.1-prefix-bottles-and-defaults/)
- [3.2 keg-only 与链接机制](3.2-keg-only-and-linking/)
- [3.3 权限模型：为什么 Homebrew 拒绝 sudo](3.3-permissions-and-sudo/)
- [3.4 Tap 第三方仓库与信任模型](3.4-taps-and-trust/)
