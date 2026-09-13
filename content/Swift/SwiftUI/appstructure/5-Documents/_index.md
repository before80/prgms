+++
title = "5 文稿"
date = 2026-09-12T12:47:47+08:00
weight = 5
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/documents](https://developer.apple.com/documentation/swiftui/documents)

# 5 文稿

让人们能够打开和管理文稿。

## 概述 {#Overview}

创建用于打开和编辑文稿的用户界面。

![](./images/documents-hero@2x.png)

使用 [ReadableDocument](https://developer.apple.com/documentation/swiftui/readabledocument) 和 [WritableDocument](https://developer.apple.com/documentation/swiftui/writabledocument) 协议来定义文稿模型；当文稿需要同时支持读写时，也可以采用把两者结合起来的便捷协议 [Document](https://developer.apple.com/documentation/swiftui/document)。这些协议让你直接访问文件 URL、与 Swift 并发集成，并支持进度报告。你也可以用 [init(editing:contentType:editor:prepareDocument:)](https://developer.apple.com/documentation/swiftui/documentgroup/init(editing:contenttype:editor:preparedocument:)) 这类构造器，使用以 SwiftData 为后端的文稿。

SwiftUI 支持人们期望基于文稿的应用具备的标准行为，并且贴合各个平台的惯例，例如多窗口支持、打开与存储面板。关于相关的设计指导，参见 Human Interface Guidelines 中的[模式](https://developer.apple.com/design/human-interface-guidelines/patterns)。

## 创建文稿 {#Creating-a-document}

- [创建基于文稿的应用](5.1-CreatingADocumentBasedApp/) —— 构建让人们能够使用协调式文件访问来打开、编辑和存储文件的应用。
- [处理高级文稿场景](5.2-HandlingAdvancedDocumentScenarios/) —— 扩展你的基于文稿的应用，支持自定义文件格式、按需文件访问和进度报告。
- [更新你的基于文稿的应用](5.3-UpdatingYourDocumentBasedApp/) —— 把一个已有应用迁移到使用 URL 的方式读写文稿，并结合 Swift 并发。
- [用 SwiftUI 构建基于文稿的应用](5.4-BuildingADocumentBasedAppWithSwiftui/) —— 在多平台应用中创建、存储和打开文稿。
- [用 SwiftData 构建基于文稿的应用](5.5-BuildingADocumentBasedAppUsingSwiftdata/) —— 跟着 WWDC 讲者一起，把一个应用改造成使用 SwiftData 的应用。
- [DocumentGroup](https://developer.apple.com/documentation/swiftui/documentgroup) —— 支持打开、创建和存储文稿的场景。

## 用引用类型实例存储文稿数据 {#Storing-document-data-in-a-reference-type-instance}

- [Document](https://developer.apple.com/documentation/swiftui/document) —— 同时支持读写的文稿。
- [ReadableDocument](https://developer.apple.com/documentation/swiftui/readabledocument) —— 支持从文件读取的文稿类型。
- [WritableDocument](https://developer.apple.com/documentation/swiftui/writabledocument) —— 支持写入文件的文稿类型。
- [URLDocumentConfiguration](https://developer.apple.com/documentation/swiftui/urldocumentconfiguration) —— 已打开文稿的配置，保存其文件 URL、最近修改日期和相关元数据。
- [DocumentCreationContext](https://developer.apple.com/documentation/swiftui/documentcreationcontext) —— 关于文稿是如何创建的上下文。
- [DocumentBaseBox](https://developer.apple.com/documentation/swiftui/documentbasebox) —— 一种 Box，允许设置其 Document 基类，而无需调用方知道 Box 及其基类的确切类型。

## 访问文稿配置 {#Accessing-document-configuration}

- [documentConfiguration](https://developer.apple.com/documentation/swiftui/environmentvalues/documentconfiguration) —— [DocumentGroup](https://developer.apple.com/documentation/swiftui/documentgroup) 中文稿的配置。
- [DocumentConfiguration](https://developer.apple.com/documentation/swiftui/documentconfiguration) —— [DocumentGroup](https://developer.apple.com/documentation/swiftui/documentgroup) 中文稿的配置。
- [undoManager](https://developer.apple.com/documentation/swiftui/environmentvalues/undomanager) —— 用来注册视图撤销操作的撤销管理器。

## 读写文稿 {#Reading-and-writing-documents}

- [DocumentReadConfiguration](https://developer.apple.com/documentation/swiftui/documentreadconfiguration) —— SwiftUI 传给 [reader(configuration:)](https://developer.apple.com/documentation/swiftui/readabledocument/reader(configuration:)) 的上下文。
- [DocumentWriteConfiguration](https://developer.apple.com/documentation/swiftui/documentwriteconfiguration) —— SwiftUI 传给 [writer(configuration:)](https://developer.apple.com/documentation/swiftui/writabledocument/writer(configuration:)) 的上下文。
- [DocumentReader](https://developer.apple.com/documentation/swiftui/documentreader) —— 从文件读取文稿内容的类型。
- [DocumentWriter](https://developer.apple.com/documentation/swiftui/documentwriter) —— 把文稿内容写入文件的类型。
- [FileWrapperDocumentReader](https://developer.apple.com/documentation/swiftui/filewrapperdocumentreader) —— 把 `FileWrapper` 反序列化为快照的文稿读取器。
- [FileWrapperDocumentWriter](https://developer.apple.com/documentation/swiftui/filewrapperdocumentwriter) —— 把快照序列化为 `FileWrapper` 的文稿写入器。

## 以编程方式打开文稿 {#Opening-a-document-programmatically}

- [newDocument](https://developer.apple.com/documentation/swiftui/environmentvalues/newdocument) —— 环境中用于呈现新文稿的动作。
- [openDocument](https://developer.apple.com/documentation/swiftui/environmentvalues/opendocument) —— 环境中用于呈现已有文稿的动作。
- [OpenDocumentAction](https://developer.apple.com/documentation/swiftui/opendocumentaction) —— 呈现已有文稿的动作。

## 配置文稿启动体验 {#Configuring-the-document-launch-experience}

- [DocumentGroupLaunchScene](https://developer.apple.com/documentation/swiftui/documentgrouplaunchscene) —— 面向基于文稿的应用的启动场景。
- [documentLaunchTitle(_:)](https://developer.apple.com/documentation/swiftui/scene/documentlaunchtitle(_:)) —— 设置文稿启动卡片上显示的标题。
- [documentLaunchSubtitle(_:)](https://developer.apple.com/documentation/swiftui/scene/documentlaunchsubtitle(_:)) —— 设置文稿启动卡片上标题下方显示的副标题。
- [DocumentLaunchView](https://developer.apple.com/documentation/swiftui/documentlaunchview) —— 启动文稿相关用户体验时呈现的视图。
- [documentLaunchTitle(_:)](https://developer.apple.com/documentation/swiftui/view/documentlaunchtitle(_:)) —— 设置文稿启动卡片上显示的标题。
- [documentLaunchSubtitle(_:)](https://developer.apple.com/documentation/swiftui/view/documentlaunchsubtitle(_:)) —— 设置文稿启动卡片上标题下方显示的副标题。
- [documentBrowserContextMenu(_:)](https://developer.apple.com/documentation/swiftui/view/documentbrowsercontextmenu(_:)) —— 为一个 `DocumentLaunchView` 添加接受所选文件列表作为参数的这些操作。
- [DocumentLaunchGeometryProxy](https://developer.apple.com/documentation/swiftui/documentlaunchgeometryproxy) —— 用于访问场景及其标题视图边框的代理。
- [DefaultDocumentGroupLaunchActions](https://developer.apple.com/documentation/swiftui/defaultdocumentgrouplaunchactions) —— 文稿组启动场景和文稿启动视图的默认操作。
- [NewDocumentButton](https://developer.apple.com/documentation/swiftui/newdocumentbutton) —— 创建并打开新文稿的按钮。
- [DefaultNewDocumentButtonLabel](https://developer.apple.com/documentation/swiftui/defaultnewdocumentbuttonlabel) —— 新文稿按钮使用的默认标签。
- [DocumentCreationSource](https://developer.apple.com/documentation/swiftui/documentcreationsource) —— 描述用于创建新文稿的来源。

## 重命名文稿 {#Renaming-a-document}

- [RenameButton](https://developer.apple.com/documentation/swiftui/renamebutton) —— 触发标准重命名操作的按钮。
- [renameAction(_:)](https://developer.apple.com/documentation/swiftui/view/renameaction(_:)) —— 设置重命名操作要运行的闭包。
- [rename](https://developer.apple.com/documentation/swiftui/environmentvalues/rename) —— 激活标准重命名交互的动作。
- [RenameAction](https://developer.apple.com/documentation/swiftui/renameaction) —— 激活标准重命名交互的动作。

## 已弃用 {#Deprecated}

- [FileDocument](https://developer.apple.com/documentation/swiftui/filedocument) —— 用于把文稿与文件之间相互序列化的类型。
- [FileDocumentConfiguration](https://developer.apple.com/documentation/swiftui/filedocumentconfiguration) —— 已打开文件文稿的属性。
- [FileDocumentReadConfiguration](https://developer.apple.com/documentation/swiftui/filedocumentreadconfiguration) —— 读取文件内容的配置。
- [FileDocumentWriteConfiguration](https://developer.apple.com/documentation/swiftui/filedocumentwriteconfiguration) —— 序列化文件内容的配置。
- [NewDocumentAction](https://developer.apple.com/documentation/swiftui/newdocumentaction) —— 呈现新文稿的动作。
- [ReferenceFileDocument](https://developer.apple.com/documentation/swiftui/referencefiledocument) —— 用于把引用类型文稿与文件之间相互序列化的类型。
- [ReferenceFileDocumentConfiguration](https://developer.apple.com/documentation/swiftui/referencefiledocumentconfiguration) —— 已打开引用类型文件文稿的属性。
