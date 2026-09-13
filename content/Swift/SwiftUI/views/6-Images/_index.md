+++
title = "6 图像"
date = 2026-09-12T12:47:47+08:00
weight = 6
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/images](https://developer.apple.com/documentation/swiftui/images)

# 6 图像

在应用界面中添加图像和符号。

## 概述 {#Overview}

用 [Image](https://developer.apple.com/documentation/swiftui/image) 视图显示图像，包括 [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)、存储在资源目录中的图像，以及存储在磁盘上的图像。

![](./images/images-hero@2x.png)

对于获取需要时间的图像——例如从网络端点加载图像——请用 [AsyncImage](https://developer.apple.com/documentation/swiftui/asyncimage) 异步加载。你可以让该视图在加载期间显示占位内容。

关于设计指导，参见 Human Interface Guidelines 中的[图像](https://developer.apple.com/design/human-interface-guidelines/images)。

## 创建图像 {#Creating-an-image}

- [Image](https://developer.apple.com/documentation/swiftui/image) —— 显示图像的视图。

## 配置图像 {#Configuring-an-image}

- [让图像适配可用空间](6.1-FittingImagesIntoAvailableSpace/) —— 通过应用视图修饰符，调整应用界面中图像的尺寸与形状。
- [imageScale(_:)](https://developer.apple.com/documentation/swiftui/view/imagescale(_:)) —— 按可用的相对尺寸之一（包括小、中、大图像尺寸）缩放视图内的图像。
- [imageScale](https://developer.apple.com/documentation/swiftui/environmentvalues/imagescale) —— 该环境的图像缩放比例。
- [Image.Scale](https://developer.apple.com/documentation/swiftui/image/scale) —— 相对于文本应用于矢量图像的缩放比例。
- [Image.Orientation](https://developer.apple.com/documentation/swiftui/image/orientation) —— 图像的方向。
- [Image.ResizingMode](https://developer.apple.com/documentation/swiftui/image/resizingmode) —— SwiftUI 用来调整图像大小以适配其容器视图的模式。

## 异步加载图像 {#Loading-images-asynchronously}

- [AsyncImage](https://developer.apple.com/documentation/swiftui/asyncimage) —— 异步加载并显示图像的视图。
- [AsyncImagePhase](https://developer.apple.com/documentation/swiftui/asyncimagephase) —— 异步图像加载操作的当前阶段。

## 设置符号变体 {#Setting-a-symbol-variant}

- [symbolVariant(_:)](https://developer.apple.com/documentation/swiftui/view/symbolvariant(_:)) —— 让视图中的符号显示某个特定变体。
- [symbolVariants](https://developer.apple.com/documentation/swiftui/environmentvalues/symbolvariants) —— 该环境中使用的符号变体。
- [SymbolVariants](https://developer.apple.com/documentation/swiftui/symbolvariants) —— 符号的变体。

## 管理符号效果 {#Managing-symbol-effects}

- [symbolEffect(_:options:isActive:)](https://developer.apple.com/documentation/swiftui/view/symboleffect(_:options:isactive:)) —— 返回一个添加了符号效果的新视图。
- [symbolEffect(_:options:value:)](https://developer.apple.com/documentation/swiftui/view/symboleffect(_:options:value:)) —— 返回一个添加了符号效果的新视图。
- [symbolEffectsRemoved(_:)](https://developer.apple.com/documentation/swiftui/view/symboleffectsremoved(_:)) —— 返回一个新视图，其继承的符号图像效果被移除或保持不变。
- [SymbolEffectTransition](https://developer.apple.com/documentation/swiftui/symboleffecttransition) —— 创建一个过渡，把出现、消失、绘制或擦除的符号动画应用到被插入或移除的视图层级中的符号图像上。

## 设置符号渲染模式 {#Setting-symbol-rendering-modes}

- [symbolRenderingMode(_:)](https://developer.apple.com/documentation/swiftui/view/symbolrenderingmode(_:)) —— 设置该视图中符号图像的渲染模式。
- [symbolRenderingMode](https://developer.apple.com/documentation/swiftui/environmentvalues/symbolrenderingmode) —— 当前的符号渲染模式；为 `nil` 表示模式会根据当前图像和前景样式自动选择。
- [SymbolRenderingMode](https://developer.apple.com/documentation/swiftui/symbolrenderingmode) —— 符号渲染模式。
- [SymbolColorRenderingMode](https://developer.apple.com/documentation/swiftui/symbolcolorrenderingmode) —— 填充符号图像中某一层的方法。
- [SymbolVariableValueMode](https://developer.apple.com/documentation/swiftui/symbolvariablevaluemode) —— 渲染符号图像变量值的方法。

## 从视图渲染图像 {#Rendering-images-from-views}

- [ImageRenderer](https://developer.apple.com/documentation/swiftui/imagerenderer) —— 从 SwiftUI 视图创建图像的对象。
