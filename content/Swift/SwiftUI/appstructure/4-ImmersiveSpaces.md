+++
title = "4 沉浸式空间"
date = 2026-09-12T12:47:47+08:00
weight = 4
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/immersive-spaces](https://developer.apple.com/documentation/swiftui/immersive-spaces)

# 4 沉浸式空间

在人的周围环境中显示无边界的沉浸内容。

## 概述 {#Overview}

在 visionOS 中使用沉浸式空间，可以在任何容器之外呈现 SwiftUI 视图。你可以在空间中放入任何视图，不过通常会使用 [RealityView](https://developer.apple.com/documentation/realitykit/realityview) 来呈现 RealityKit 内容。

![](./images/immersive-spaces-hero@2x.png)

你可以用 [immersionStyle(selection:in:)](https://developer.apple.com/documentation/swiftui/scene/immersionstyle(selection:in:)) 场景修饰符请求三种空间样式之一：

- [mixed](https://developer.apple.com/documentation/swiftui/immersionstyle/mixed)（混合）样式把你的内容与透视画面融合在一起。这让你可以把虚拟物体放置在人的周围环境中。
- [full](https://developer.apple.com/documentation/swiftui/immersionstyle/full)（完全）样式只显示你的内容，关闭透视画面。这让你可以完全控制视觉体验，例如把人们带到另一个世界。
- [progressive](https://developer.apple.com/documentation/swiftui/immersionstyle/progressive)（渐进）样式在显示区域的一部分完全取代透视画面。你可以用这种样式在展示另一个世界的同时，让人们仍然立足现实世界。

当你打开一个沉浸式空间时，系统会继续显示你应用的所有窗口，但会隐藏其他应用的窗口。系统在所有应用之间只支持同时显示一个空间，因此只有在没有其他空间打开时，你的应用才能打开空间。

## 创建沉浸式空间 {#Creating-an-immersive-space}

- [ImmersiveSpace](https://developer.apple.com/documentation/swiftui/immersivespace) —— 在无边界空间中呈现其内容的场景。
- [ImmersiveSpaceContentBuilder](https://developer.apple.com/documentation/swiftui/immersivespacecontentbuilder) —— 用于把一组沉浸式空间元素组合起来的结果构建器。
- [immersionStyle(selection:in:)](https://developer.apple.com/documentation/swiftui/scene/immersionstyle(selection:in:)) —— 设置沉浸式空间的样式。
- [ImmersionStyle](https://developer.apple.com/documentation/swiftui/immersionstyle) —— 沉浸式空间可以具有的样式。
- [immersiveSpaceDisplacement](https://developer.apple.com/documentation/swiftui/environmentvalues/immersivespacedisplacement) —— 当空间被移离默认位置时，系统对该沉浸式空间施加的位移（以米为单位）。
- [ImmersiveEnvironmentBehavior](https://developer.apple.com/documentation/swiftui/immersiveenvironmentbehavior) —— 当你的应用打开场景时，系统提供的沉浸式环境的行为。
- [ProgressiveImmersionAspectRatio](https://developer.apple.com/documentation/swiftui/progressiveimmersionaspectratio)

## 打开沉浸式空间 {#Opening-an-immersive-space}

- [openImmersiveSpace](https://developer.apple.com/documentation/swiftui/environmentvalues/openimmersivespace) —— 呈现沉浸式空间的动作。
- [OpenImmersiveSpaceAction](https://developer.apple.com/documentation/swiftui/openimmersivespaceaction) —— 呈现沉浸式空间的动作。

## 关闭沉浸式空间 {#Closing-the-immersive-space}

- [dismissImmersiveSpace](https://developer.apple.com/documentation/swiftui/environmentvalues/dismissimmersivespace) —— 存储在视图环境中的沉浸式空间关闭动作。
- [DismissImmersiveSpaceAction](https://developer.apple.com/documentation/swiftui/dismissimmersivespaceaction) —— 关闭沉浸式空间的动作。

## 沉浸期间隐藏上肢 {#Hiding-upper-limbs-during-immersion}

- [upperLimbVisibility(_:)](https://developer.apple.com/documentation/swiftui/scene/upperlimbvisibility(_:)) —— 在呈现 [ImmersiveSpace](https://developer.apple.com/documentation/swiftui/immersivespace) 场景时，设置用户上肢的偏好可见性。
- [upperLimbVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/upperlimbvisibility(_:)) —— 在呈现 [ImmersiveSpace](https://developer.apple.com/documentation/swiftui/immersivespace) 场景时，设置用户上肢的偏好可见性。

## 调整内容亮度 {#Adjusting-content-brightness}

- [immersiveContentBrightness(_:)](https://developer.apple.com/documentation/swiftui/scene/immersivecontentbrightness(_:)) —— 设置沉浸式空间的内容亮度。
- [ImmersiveContentBrightness](https://developer.apple.com/documentation/swiftui/immersivecontentbrightness) —— 沉浸式空间的内容亮度。

## 响应沉浸状态变化 {#Responding-to-immersion-changes}

- [onImmersionChange(initial:_:)](https://developer.apple.com/documentation/swiftui/view/onimmersionchange(initial:_:)) —— 当应用的沉浸状态发生变化时执行一个动作。
- [ImmersionChangeContext](https://developer.apple.com/documentation/swiftui/immersionchangecontext) —— 表示应用沉浸状态的结构体。

## 向沉浸式空间添加菜单项 {#Adding-menu-items-to-an-immersive-space}

- [immersiveEnvironmentPicker(content:)](https://developer.apple.com/documentation/swiftui/view/immersiveenvironmentpicker(content:)) —— 向媒体播放器的环境选择器添加菜单项，用于打开沉浸式空间。

## 处理远程沉浸式空间 {#Handling-remote-immersive-spaces}

- [RemoteImmersiveSpace](https://developer.apple.com/documentation/swiftui/remoteimmersivespace) —— 在远程设备的无边界空间中呈现其内容的场景。
- [RemoteDeviceIdentifier](https://developer.apple.com/documentation/swiftui/remotedeviceidentifier) —— 一种不透明类型，用来标识在 [RemoteImmersiveSpace](https://developer.apple.com/documentation/swiftui/remoteimmersivespace) 中显示场景内容的远程设备。
