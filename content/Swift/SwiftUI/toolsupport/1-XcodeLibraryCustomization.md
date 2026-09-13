+++
title = "1 Xcode 资源库自定义"
date = 2026-09-12T12:47:47+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/xcode-library-customization](https://developer.apple.com/documentation/swiftui/xcode-library-customization)

# 1 Xcode 资源库自定义

在 Xcode 资源库中公开你的自定义视图和修饰符。

## 概述 {#Overview}

你可以把自己的自定义 SwiftUI 视图和视图修饰符加入 Xcode 的资源库。这样，任何开发你的应用或采用你的框架的人，都可以通过点按 Xcode 工具栏中的资源库按钮（+）来访问它们。你可以像使用系统提供的项目那样，选中并把自定义资源库项目拖入代码中。

![](./images/xcode-library-customization-hero@2x.png)

要把项目加入资源库，请创建一个遵循 [LibraryContentProvider](https://developer.apple.com/documentation/developertoolssupport/librarycontentprovider) 协议的结构体，并把你想要添加的任何项目封装为 [LibraryItem](https://developer.apple.com/documentation/developertoolssupport/libraryitem) 实例。实现 [views](https://developer.apple.com/documentation/developertoolssupport/librarycontentprovider/views) 计算属性来添加包含视图的资源库项目。实现 [modifiers(base:)](https://developer.apple.com/documentation/developertoolssupport/librarycontentprovider/modifiers(base:)) 方法来添加包含视图修饰符的项目。Xcode 会在你工作时从项目中的所有资源库内容提供者收集项目，并让它们在你的资源库中可用。

## 创建资源库项目 {#Creating-library-items}

- [LibraryContentProvider](https://developer.apple.com/documentation/developertoolssupport/librarycontentprovider) — Xcode 资源库和代码补全内容的来源。
- [LibraryItem](https://developer.apple.com/documentation/developertoolssupport/libraryitem) — 要加入 Xcode 资源库的单个项目。
