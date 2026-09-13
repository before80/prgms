+++
title = "1.3 Xcode 中的预览"
date = 2026-09-12T12:47:47+08:00
weight = 3
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/previews-in-xcode](https://developer.apple.com/documentation/swiftui/previews-in-xcode)

# 1.3 Xcode 中的预览

为自定义视图生成动态、可交互的预览。

## 概述 {#Overview}

当你用 SwiftUI 创建自定义 [View](https://developer.apple.com/documentation/swiftui/view) 时，Xcode 可以显示该视图内容的预览，并随着你修改视图代码保持更新。你使用某个预览宏——例如 [Preview(_:body:)](https://developer.apple.com/documentation/swiftui/preview(_:body:))——告诉 Xcode 要显示什么。Xcode 会在代码旁的画布中显示预览。

![](./images/previews-in-xcode-hero@2x.png)

不同的预览宏支持不同种类的配置。例如，你可以用 [Preview(_:traits:_:body:)](https://developer.apple.com/documentation/swiftui/preview(_:traits:_:body:)) 宏添加影响预览外观的特性，或者用 [Preview(_:traits:body:cameras:)](https://developer.apple.com/documentation/swiftui/preview(_:traits:body:cameras:)) 宏为预览添加自定义视点。你也可以检查视图在特定场景类型中的行为。例如在 visionOS 中，你可以用 [Preview(_:immersionStyle:traits:body:)](https://developer.apple.com/documentation/swiftui/preview(_:immersionstyle:traits:body:)) 宏在 [ImmersiveSpace](https://developer.apple.com/documentation/swiftui/immersivespace) 中预览视图。

## 基础 {#Essentials}

- [为界面文件添加预览](https://developer.apple.com/documentation/xcode/adding-previews-to-your-interface-files) —— 编写代码以在不同设备和配置上测试视图，而无需运行应用。

## 创建预览 {#Creating-a-preview}

- [Preview(_:body:)](https://developer.apple.com/documentation/swiftui/preview(_:body:)) —— 创建 SwiftUI 视图的预览。
- [Preview(_:traits:_:body:)](https://developer.apple.com/documentation/swiftui/preview(_:traits:_:body:)) —— 用指定的特性创建 SwiftUI 视图的预览。
- [Preview(_:traits:body:cameras:)](https://developer.apple.com/documentation/swiftui/preview(_:traits:body:cameras:)) —— 用指定的特性和自定义视点创建 SwiftUI 视图的预览。
- [Preview(_:traits:arguments:body:)](https://developer.apple.com/documentation/swiftui/preview(_:traits:arguments:body:)) —— 为一组参数化的 SwiftUI 视图创建预览，让它的输入在所提供的一组实参上变化。

## 自定义预览 {#Customizing-a-preview}

- [Previewable()](https://developer.apple.com/documentation/swiftui/previewable()) —— 允许动态属性内联出现在预览中的标记。
- [PreviewModifier](https://developer.apple.com/documentation/swiftui/previewmodifier) —— 定义预览所处环境的类型。
- [PreviewModifierContent](https://developer.apple.com/documentation/swiftui/previewmodifiercontent) —— 类型擦除的预览内容。

## 在场景上下文中创建预览 {#Creating-a-preview-in-the-context-of-a-scene}

- [Preview(_:immersionStyle:traits:body:)](https://developer.apple.com/documentation/swiftui/preview(_:immersionstyle:traits:body:)) —— 在沉浸式空间中创建 SwiftUI 视图的预览。
- [Preview(_:immersionStyle:traits:body:cameras:)](https://developer.apple.com/documentation/swiftui/preview(_:immersionstyle:traits:body:cameras:)) —— 在带自定义视点的沉浸式空间中创建 SwiftUI 视图的预览。
- [Preview(_:windowStyle:traits:body:)](https://developer.apple.com/documentation/swiftui/preview(_:windowstyle:traits:body:)) —— 在窗口中创建 SwiftUI 视图的预览。
- [Preview(_:windowStyle:traits:body:cameras:)](https://developer.apple.com/documentation/swiftui/preview(_:windowstyle:traits:body:cameras:)) —— 在带自定义视点的窗口中创建 SwiftUI 视图的预览。

## 在调试模式下构建 {#Building-in-debug-mode}

- [DebugReplaceableView](https://developer.apple.com/documentation/swiftui/debugreplaceableview) —— 在调试构建中擦除视图的不透明结果类型。

## 已弃用 {#Deprecated}

- [已弃用](1.3.1-PreviewsDeprecated/) —— 查阅已弃用的预览符号及其替代方案。
