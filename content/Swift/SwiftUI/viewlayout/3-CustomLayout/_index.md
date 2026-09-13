+++
title = "3 自定义布局"
date = 2026-09-12T12:47:47+08:00
weight = 3
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/custom-layout](https://developer.apple.com/documentation/swiftui/custom-layout)

# 3 自定义布局

按自定义方式排列视图，并在不同布局类型之间创建动画过渡。

## 概述 {#Overview}

你可以用 SwiftUI 提供的内置布局容器和布局视图修饰符创建复杂的视图布局。不过，如果你需要某种内置布局工具无法实现的行为，可以用 [Layout](https://developer.apple.com/documentation/swiftui/layout) 协议创建自定义布局容器类型。你定义的容器会先询问所有子视图的尺寸，然后指明把这些子视图放在自身边界内的什么位置。

![](./images/custom-layout-hero@2x.png)

你还可以在遵循 [Layout](https://developer.apple.com/documentation/swiftui/layout) 协议的各种布局类型（包括内置布局和自定义布局）之间创建动画过渡。

关于设计指导，请参阅 Human Interface Guidelines 中的 [布局](https://developer.apple.com/design/human-interface-guidelines/layout)。

## 创建自定义布局容器 {#Creating-a-custom-layout-container}

- [用 SwiftUI 组合自定义布局](3.1-ComposingCustomLayoutsWithSwiftui/) — 使用 SwiftUI 提供的布局工具来排列应用界面中的视图。
- [Layout](https://developer.apple.com/documentation/swiftui/layout) — 一种定义一组视图的几何信息的类型。
- [LayoutSubview](https://developer.apple.com/documentation/swiftui/layoutsubview) — 表示布局中某个子视图的代理。
- [LayoutSubviews](https://developer.apple.com/documentation/swiftui/layoutsubviews) — 一组表示布局视图各个子视图的代理值。

## 配置自定义布局 {#Configuring-a-custom-layout}

- [LayoutProperties](https://developer.apple.com/documentation/swiftui/layoutproperties) — 布局容器特有的布局属性。
- [ProposedViewSize](https://developer.apple.com/documentation/swiftui/proposedviewsize) — 对视图尺寸的提议。
- [ViewSpacing](https://developer.apple.com/documentation/swiftui/viewspacing) — 视图的几何间距偏好集合。

## 在自定义布局中把值与视图关联 {#Associating-values-with-views-in-a-custom-layout}

- [layoutValue(key:value:)](https://developer.apple.com/documentation/swiftui/view/layoutvalue(key:value:)) — 把一个值与自定义布局属性关联起来。
- [LayoutValueKey](https://developer.apple.com/documentation/swiftui/layoutvaluekey) — 用于访问布局容器子视图的布局值的键。

## 在布局类型之间过渡 {#Transitioning-between-layout-types}

- [AnyLayout](https://developer.apple.com/documentation/swiftui/anylayout) — 类型被抹除的布局协议实例。
- [HStackLayout](https://developer.apple.com/documentation/swiftui/hstacklayout) — 一种可用于条件布局的水平容器。
- [VStackLayout](https://developer.apple.com/documentation/swiftui/vstacklayout) — 一种可用于条件布局的垂直容器。
- [ZStackLayout](https://developer.apple.com/documentation/swiftui/zstacklayout) — 一种可用于条件布局的叠加容器。
- [GridLayout](https://developer.apple.com/documentation/swiftui/gridlayout) — 一种可用于条件布局的网格。
