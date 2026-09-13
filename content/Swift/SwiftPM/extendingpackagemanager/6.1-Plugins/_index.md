+++
title = "6.1 插件"
date = 2026-09-11T21:45:00+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://docs.swift.org/latest/documentation/packagemanagerdocs/plugins/](https://docs.swift.org/latest/documentation/packagemanagerdocs/plugins/)

# 6.1 插件

用构建插件或命令插件扩展包管理器的功能。

## 概述 {#Overview}

Swift Package Manager 的部分功能可以通过*插件*来扩展。使用 Swift Package Manager 提供的 `PackagePlugin` API 编写包插件。这与包清单文件的实现方式类似——都是 Swift 代码，在需要时运行以产出包管理器所需的信息。

包管理器为插件定义了两个扩展点：

- 构建插件：自定义的构建工具任务，提供在构建之前或构建期间运行的命令。参见[启用构建插件](6.1.2-EnableBuildPlugin/)了解如何添加已有的构建插件，或者参见[编写构建工具插件](6.1.4-WritingBuildToolPlugin/)了解如何编写自己的插件。

- 命令插件：自定义命令，你用 `swift package` 命令行接口来运行它们。参见[启用命令插件](6.1.1-EnableCommandPlugin/)了解如何添加已有的命令插件，或者参见[编写命令插件](6.1.3-WritingCommandPlugin/)了解如何编写自己的插件。

### 插件的能力 {#Plugin-Capabilities}

插件可以访问包模型的一份表示。命令插件还可以调用包管理器提供的服务，来构建和测试插件所作用的包中定义的产品和目标。

每个插件都作为独立于包管理器的进程运行。在支持沙箱的平台上，包管理器会把插件包在沙箱中，阻止网络访问，并阻止它尝试写入文件系统中的任意位置。所有插件都可以写入一个临时目录。

需要修改包源代码的自定义命令插件可以声明这一需求。如果用户批准，包管理器会授予对包目录的写权限。构建工具插件不能修改包源代码。

### 创建插件 {#Creating-Plugins}

创建插件时，在包清单中把插件表示为 `pluginTarget` 类型的目标。如果它还需要供其他包使用，则再包含一个对应的 `pluginProduct` 目标。插件的源代码通常位于包中 `Plugins` 目录下的某个目录里，但这个位置可以自定义。

插件通过定义自己的*能力*（capability）来声明它实现的是哪个扩展点。这决定了包管理器调用它的入口点，也决定了该插件可以执行哪些操作。

### 参考资料 {#References}

- "Meet Swift Package plugins" [WWDC22 session](https://developer.apple.com/videos/play/wwdc2022-110359)
- "Create Swift Package plugins" [WWDC22 session](https://developer.apple.com/videos/play/wwdc2022-110401)
