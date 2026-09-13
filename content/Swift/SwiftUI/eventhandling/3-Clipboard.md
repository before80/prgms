+++
title = "3 剪贴板"
date = 2026-09-12T12:47:47+08:00
weight = 3
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/clipboard](https://developer.apple.com/documentation/swiftui/clipboard)

# 3 剪贴板

让大家能够通过执行“拷贝”和“粘贴”命令来移动或复制项目。

## 概述 {#Overview}

当人们执行标准的“拷贝”和“剪切”命令时，他们期望把项目移动到系统剪贴板，之后可以再把项目粘贴到同一应用中的其他位置，或粘贴到另一个应用中。只要添加用于指明如何响应这些标准命令的视图修饰符，你的应用就能参与这项活动。

![](./images/clipboard-hero@2x.png)

在你的拷贝与粘贴修饰符中，提供或接受遵循 [Transferable](https://developer.apple.com/documentation/coretransferable/transferable) 协议的类型，或者继承自 [NSItemProvider](https://developer.apple.com/documentation/foundation/nsitemprovider) 类的类型。在可能的情况下，优先使用可传输的项目。

## 拷贝可传输的项目 {#Copying-transferable-items}

- [copyable(_:)](https://developer.apple.com/documentation/swiftui/view/copyable(_:)) — 指定在系统执行“拷贝”命令时要拷贝的项目列表。
- [cuttable(for:action:)](https://developer.apple.com/documentation/swiftui/view/cuttable(for:action:)) — 指定一个动作，在系统执行“剪切”命令时把项目移动到剪贴板。
- [pasteDestination(for:action:validator:)](https://developer.apple.com/documentation/swiftui/view/pastedestination(for:action:validator:)) — 指定一个动作，在系统执行“粘贴”命令时把经过验证的项目添加到视图中。

## 使用项目提供者拷贝项目 {#Copying-items-using-item-providers}

- [onCopyCommand(perform:)](https://developer.apple.com/documentation/swiftui/view/oncopycommand(perform:)) — 添加一个动作，以响应系统发出的“拷贝”命令。
- [onCutCommand(perform:)](https://developer.apple.com/documentation/swiftui/view/oncutcommand(perform:)) — 添加一个动作，以响应系统发出的“剪切”命令。
- [onPasteCommand(of:perform:)](https://developer.apple.com/documentation/swiftui/view/onpastecommand(of:perform:)) — 添加一个动作，以响应系统发出的“粘贴”命令。
- [onPasteCommand(of:validator:perform:)](https://developer.apple.com/documentation/swiftui/view/onpastecommand(of:validator:perform:)) — 添加一个动作，以响应系统发出的“粘贴”命令，并处理由你验证过的项目。
