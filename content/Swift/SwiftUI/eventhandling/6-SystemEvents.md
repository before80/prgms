+++
title = "6 系统事件"
date = 2026-09-12T12:47:47+08:00
weight = 6
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/system-events](https://developer.apple.com/documentation/swiftui/system-events)

# 6 系统事件

响应打开 URL 等系统事件。

## 概述 {#Overview}

指定视图和场景修饰符，可以指明应用如何响应某些系统事件。例如，你可以用 [onOpenURL(perform:)](https://developer.apple.com/documentation/swiftui/view/onopenurl(perform:)) 视图修饰符定义一个动作，当应用收到通用链接时执行；也可以用 [backgroundTask(_:action:)](https://developer.apple.com/documentation/swiftui/scene/backgroundtask(_:action:)) 场景修饰符指定一个异步任务，以响应后台任务事件（例如后台 URL 会话完成）。

![](./images/system-events-hero@2x.png)

## 发送和接收用户活动 {#Sending-and-receiving-user-activities}

- [用 SwiftUI 恢复应用状态](../../datastorage/4-PersistentStorage/4.1-RestoringYourAppSStateWithSwiftui/) — 通过保留用户当前的活动，为用户提供应用连续性。
- [userActivity(_:element:_:)](https://developer.apple.com/documentation/swiftui/view/useractivity(_:element:_:)) — 声明某种用户活动类型。
- [userActivity(_:isActive:_:)](https://developer.apple.com/documentation/swiftui/view/useractivity(_:isactive:_:)) — 声明某种用户活动类型。
- [onContinueUserActivity(_:perform:)](https://developer.apple.com/documentation/swiftui/view/oncontinueuseractivity(_:perform:)) — 注册一个处理器，以响应应用收到的用户活动。

## 发送和接收 URL {#Sending-and-receiving-URLs}

- [openURL](https://developer.apple.com/documentation/swiftui/environmentvalues/openurl) — 一个打开 URL 的动作。
- [OpenURLAction](https://developer.apple.com/documentation/swiftui/openurlaction) — 一个打开 URL 的动作。
- [onOpenURL(perform:)](https://developer.apple.com/documentation/swiftui/view/onopenurl(perform:)) — 注册一个处理器，以响应应用收到的 URL。

## 处理外部事件 {#Handling-external-events}

- [handlesExternalEvents(matching:)](https://developer.apple.com/documentation/swiftui/scene/handlesexternalevents(matching:)) — 指定哪些外部事件会让 SwiftUI 打开被修改场景的新实例。
- [handlesExternalEvents(preferring:allowing:)](https://developer.apple.com/documentation/swiftui/view/handlesexternalevents(preferring:allowing:)) — 在场景已经打开的情况下，指定该视图所在场景处理哪些外部事件。

## 处理后台任务 {#Handling-background-tasks}

- [backgroundTask(_:action:)](https://developer.apple.com/documentation/swiftui/scene/backgroundtask(_:action:)) — 当系统提供后台任务时运行指定的动作。
- [BackgroundTask](https://developer.apple.com/documentation/swiftui/backgroundtask) — 你的应用或扩展可以处理的后台任务种类。
- [SnapshotData](https://developer.apple.com/documentation/swiftui/snapshotdata) — 快照后台任务的关联数据。
- [SnapshotResponse](https://developer.apple.com/documentation/swiftui/snapshotresponse) — 应用对快照后台任务的响应。

## 导入和导出可传输项目 {#Importing-and-exporting-transferable-items}

- [importableFromServices(for:action:)](https://developer.apple.com/documentation/swiftui/view/importablefromservices(for:action:)) — 允许从服务导入项目，例如 macOS 上的“接续互通相机”。
- [exportableToServices(_:)](https://developer.apple.com/documentation/swiftui/view/exportabletoservices(_:)) — 导出项目以供快捷指令、快速操作和服务使用。
- [exportableToServices(_:onEdit:)](https://developer.apple.com/documentation/swiftui/view/exportabletoservices(_:onedit:)) — 导出可读写项目以供快捷指令、快速操作和服务使用。

## 使用项目提供者导入和导出 {#Importing-and-exporting-using-item-providers}

- [importsItemProviders(_:onImport:)](https://developer.apple.com/documentation/swiftui/view/importsitemproviders(_:onimport:)) — 允许从服务导入项目提供者，例如 macOS 上的“接续互通相机”。
- [exportsItemProviders(_:onExport:)](https://developer.apple.com/documentation/swiftui/view/exportsitemproviders(_:onexport:)) — 导出一个只读项目提供者，以供快捷指令、快速操作和服务使用。
- [exportsItemProviders(_:onExport:onEdit:)](https://developer.apple.com/documentation/swiftui/view/exportsitemproviders(_:onexport:onedit:)) — 导出一个可读写项目提供者，以供快捷指令、快速操作和服务使用。
