+++
title = "5 无障碍导航"
date = 2026-09-12T12:47:47+08:00
weight = 5
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/accessible-navigation](https://developer.apple.com/documentation/swiftui/accessible-navigation)

# 5 无障碍导航

让用户可以使用转子导航到特定的用户界面元素。

## 概述 {#Overview}

辅助功能转子是一种快捷方式，让用户可以快速导航到用户界面中的特定元素，并可选地导航到这些元素内部的特定文本范围。

![](./images/accessible-navigation-hero@2x.png)

系统会自动为许多可导航元素提供转子，但你也可以为特定目的提供额外的转子，或者在系统转子无法自动获取屏幕外元素（例如 [LazyVStack](https://developer.apple.com/documentation/swiftui/lazyvstack) 或 [List](https://developer.apple.com/documentation/swiftui/list) 中位置很靠下的元素）时替换它们。

关于设计指导，请参阅 Human Interface Guidelines 辅助功能部分中的 [辅助功能](https://developer.apple.com/design/human-interface-guidelines/accessibility)。

## 使用转子 {#Working-with-rotors}

- [accessibilityRotor(_:entries:)](https://developer.apple.com/documentation/swiftui/view/accessibilityrotor(_:entries:)) — 用指定的用户可见标签以及由内容闭包生成的条目，创建一个辅助功能转子。
- [accessibilityRotor(_:entries:entryID:entryLabel:)](https://developer.apple.com/documentation/swiftui/view/accessibilityrotor(_:entries:entryid:entrylabel:)) — 用指定的用户可见标签和条目创建一个辅助功能转子。
- [accessibilityRotor(_:entries:entryLabel:)](https://developer.apple.com/documentation/swiftui/view/accessibilityrotor(_:entries:entrylabel:)) — 用指定的用户可见标签和条目创建一个辅助功能转子。
- [accessibilityRotor(_:textRanges:)](https://developer.apple.com/documentation/swiftui/view/accessibilityrotor(_:textranges:)) — 用指定的用户可见标签以及为各个指定范围创建的条目，创建一个辅助功能转子。该转子会附加到当前的辅助功能元素上，每个条目会指向该元素中指定的范围。

## 创建转子 {#Creating-rotors}

- [AccessibilityRotorContent](https://developer.apple.com/documentation/swiftui/accessibilityrotorcontent) — 辅助功能转子中的内容。
- [AccessibilityRotorContentBuilder](https://developer.apple.com/documentation/swiftui/accessibilityrotorcontentbuilder) — 用于生成转子条目内容的结果构建器。
- [AccessibilityRotorEntry](https://developer.apple.com/documentation/swiftui/accessibilityrotorentry) — 表示辅助功能转子中某个条目的结构体。

## 替换系统转子 {#Replacing-system-rotors}

- [AccessibilitySystemRotor](https://developer.apple.com/documentation/swiftui/accessibilitysystemrotor) — 指定用开发者提供的转子替换系统自动提供的某个转子。

## 配置转子 {#Configuring-rotors}

- [accessibilityRotorEntry(id:in:)](https://developer.apple.com/documentation/swiftui/view/accessibilityrotorentry(id:in:)) — 定义一个显式标识符，把该视图的辅助功能元素与辅助功能转子中的某个条目关联起来。
- [accessibilityLinkedGroup(id:in:)](https://developer.apple.com/documentation/swiftui/view/accessibilitylinkedgroup(id:in:)) — 把多个辅助功能元素关联起来，让用户可以快速从一个元素导航到另一个元素，即使这些元素在辅助功能层级中相距较远也没问题。
- [accessibilitySortPriority(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilitysortpriority(_:)) — 设置该视图辅助功能元素相对于同一层级其他元素的排序优先级。
