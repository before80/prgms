+++
title = "7.4 swift sdk"
date = 2026-09-11T21:45:00+08:00
weight = 4
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://docs.swift.org/latest/documentation/packagemanagerdocs/swiftsdkcommands/](https://docs.swift.org/latest/documentation/packagemanagerdocs/swiftsdkcommands/)

# 7.4 swift sdk

对 Swift SDK 执行操作。

## 概述 {#Overview}

默认情况下，Swift Package Manager 为你运行它的宿主机平台编译代码。Swift 6.1 通过 [SE-0387](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0387-cross-compilation-destinations.md) 引入了 SDK，以支持交叉编译。

SDK 与用来创建它们的工具链紧密耦合。受支持的 SDK 由 Swift 项目分发，macOS 和 Linux 的下载链接见[安装页面](https://www.swift.org/install/)，Windows 的则包含在发行版中。

此外，Swift 项目还提供了工具仓库 [swift-sdk-generator](https://github.com/swiftlang/swift-sdk-generator)，你可以用它为自己偏好的平台创建自定义 SDK。
