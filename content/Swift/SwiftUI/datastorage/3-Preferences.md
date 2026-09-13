+++
title = "3 偏好设置"
date = 2026-09-12T12:47:47+08:00
weight = 3
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/preferences](https://developer.apple.com/documentation/swiftui/preferences)

# 3 偏好设置

把配置偏好从视图传递给容纳它们的容器视图。

## 概述 {#Overview}

环境用于配置某个视图的子视图，而偏好设置则用于把配置信息从子视图向上发送给容器。不过，与从一个容器向下流向众多子视图的配置信息不同，单个容器需要协调从众多子视图向上流动的、可能相互冲突的偏好设置。

![](./images/preferences-hero@2x.png)

当你用 [PreferenceKey](https://developer.apple.com/documentation/swiftui/preferencekey) 协议定义自定义偏好时，就指明了如何合并来自多个子视图的偏好。然后你可以用 [preference(key:value:)](https://developer.apple.com/documentation/swiftui/view/preference(key:value:)) 视图修饰符为某个视图设置该偏好的值。许多内置修饰符（例如 [navigationTitle(_:)](https://developer.apple.com/documentation/swiftui/view/navigationtitle(_:))）都依赖偏好设置把配置信息发送给它们的容器。

## 设置偏好 {#Setting-preferences}

- [preference(key:value:)](https://developer.apple.com/documentation/swiftui/view/preference(key:value:)) —— 为给定偏好设置一个值。
- [transformPreference(_:_:)](https://developer.apple.com/documentation/swiftui/view/transformpreference(_:_:)) —— 对某个偏好值应用一次变换。

## 创建自定义偏好 {#Creating-custom-preferences}

- [PreferenceKey](https://developer.apple.com/documentation/swiftui/preferencekey) —— 由视图产生的具名值。

## 基于几何信息设置偏好 {#Setting-preferences-based-on-geometry}

- [anchorPreference(key:value:transform:)](https://developer.apple.com/documentation/swiftui/view/anchorpreference(key:value:transform:)) —— 为指定的偏好键设置一个值，该值是与当前坐标空间关联的几何值的函数，使该值的读取者可以把几何信息转换到自己的本地坐标中。
- [transformAnchorPreference(key:value:transform:)](https://developer.apple.com/documentation/swiftui/view/transformanchorpreference(key:value:transform:)) —— 为指定的偏好键设置一个值，该值是键的当前值与绑定到当前坐标空间的几何值的函数，使该值的读取者可以把几何信息转换到自己的本地坐标中。

## 响应偏好变化 {#Responding-to-changes-in-preferences}

- [onPreferenceChange(_:perform:)](https://developer.apple.com/documentation/swiftui/view/onpreferencechange(_:perform:)) —— 添加当指定偏好键的值变化时要执行的动作。

## 由偏好生成背景与叠加层 {#Generating-backgrounds-and-overlays-from-preferences}

- [backgroundPreferenceValue(_:_:)](https://developer.apple.com/documentation/swiftui/view/backgroundpreferencevalue(_:_:)) —— 从视图中读取指定的偏好值，用它生成第二个视图，并把它作为原视图的背景。
- [backgroundPreferenceValue(_:alignment:_:)](https://developer.apple.com/documentation/swiftui/view/backgroundpreferencevalue(_:alignment:_:)) —— 从视图中读取指定的偏好值，用它生成第二个视图，并把它作为原视图的背景。
- [overlayPreferenceValue(_:_:)](https://developer.apple.com/documentation/swiftui/view/overlaypreferencevalue(_:_:)) —— 从视图中读取指定的偏好值，用它生成第二个视图，并把它作为原视图的叠加层。
- [overlayPreferenceValue(_:alignment:_:)](https://developer.apple.com/documentation/swiftui/view/overlaypreferencevalue(_:alignment:_:)) —— 从视图中读取指定的偏好值，用它生成第二个视图，并把它作为原视图的叠加层。
