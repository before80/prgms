+++
title = "3 WatchKit 集成"
date = 2026-09-12T12:47:47+08:00
weight = 3
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/watchkit-integration](https://developer.apple.com/documentation/swiftui/watchkit-integration)

# 3 WatchKit 集成

把 WatchKit 视图加入你的 SwiftUI 应用，或者在 WatchKit 应用中使用 SwiftUI 视图。

## 概述 {#Overview}

使用托管控制器把 SwiftUI 与应用的现有内容集成起来，从而把 SwiftUI 视图加入 WatchKit 界面。托管控制器会包装一组 SwiftUI 视图，其形式可以让你随后把它加入到基于故事板的应用中。

![](./images/watchkit-integration-hero@2x.png)

你也可以把 WatchKit 视图和视图控制器加入你的 SwiftUI 界面。representable 对象会包装指定的视图或视图控制器，并促进被包装对象与你的 SwiftUI 视图之间的通信。

关于设计指导，请参阅 Human Interface Guidelines 中的 [为 watchOS 设计](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos)。

## 在 WatchKit 中显示 SwiftUI 视图 {#Displaying-SwiftUI-views-in-WatchKit}

- [WKHostingController](https://developer.apple.com/documentation/swiftui/wkhostingcontroller) — 一种托管 SwiftUI 视图层级的 WatchKit 界面控制器。
- [WKUserNotificationHostingController](https://developer.apple.com/documentation/swiftui/wkusernotificationhostingcontroller) — 一种托管 SwiftUI 视图层级的 WatchKit 用户通知界面控制器。

## 把 WatchKit 视图加入 SwiftUI 视图层级 {#Adding-WatchKit-views-to-SwiftUI-view-hierarchies}

- [WKInterfaceObjectRepresentable](https://developer.apple.com/documentation/swiftui/wkinterfaceobjectrepresentable) — 一种表示 WatchKit 界面对象的视图。
- [WKInterfaceObjectRepresentableContext](https://developer.apple.com/documentation/swiftui/wkinterfaceobjectrepresentablecontext) — 关于系统状态的上下文信息，你在创建和更新 WatchKit 界面对象时使用它。
