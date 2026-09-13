+++
title = "4 无障碍描述"
date = 2026-09-12T12:47:47+08:00
weight = 4
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/accessible-descriptions](https://developer.apple.com/documentation/swiftui/accessible-descriptions)

# 4 无障碍描述

描述界面元素，帮助人们理解它们代表什么。

## 概述 {#Overview}

SwiftUI 通常可以推断出关于用户界面元素的一些信息，但你可以使用辅助功能修饰符，为需要这些信息的用户提供更多内容。

![](./images/accessible-descriptions-hero@2x.png)

关于设计指导，请参阅 Human Interface Guidelines 辅助功能部分中的 [辅助功能](https://developer.apple.com/design/human-interface-guidelines/accessibility)。

## 应用标签 {#Applying-labels}

- [accessibilityLabel(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilitylabel(_:)) — 为视图添加一个描述其内容的标签。
- [accessibilityLabel(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilitylabel(_:isenabled:)) — 为视图添加一个描述其内容的标签。
- [accessibilityLabel(content:)](https://developer.apple.com/documentation/swiftui/view/accessibilitylabel(content:)) — 为视图添加一个描述其内容的标签。
- [accessibilityInputLabels(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityinputlabels(_:)) — 设置用户用来标识某个视图的备用输入标签。
- [accessibilityInputLabels(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilityinputlabels(_:isenabled:)) — 设置用户用来标识某个视图的备用输入标签。
- [accessibilityLabeledPair(role:id:in:)](https://developer.apple.com/documentation/swiftui/view/accessibilitylabeledpair(role:id:in:)) — 把表示标签的辅助功能元素与对应内容的元素配对。
- [AccessibilityLabeledPairRole](https://developer.apple.com/documentation/swiftui/accessibilitylabeledpairrole) — 辅助功能元素在标签/内容配对中的角色。

## 描述值 {#Describing-values}

- [accessibilityValue(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityvalue(_:)) — 添加对视图所含值的文本描述。
- [accessibilityValue(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilityvalue(_:isenabled:)) — 添加对视图所含值的文本描述。

## 描述内容 {#Describing-content}

- [accessibilityTextContentType(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilitytextcontenttype(_:)) — 设置辅助功能文本内容类型。
- [accessibilityHeading(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityheading(_:)) — 设置该标题的辅助功能层级。
- [AccessibilityHeadingLevel](https://developer.apple.com/documentation/swiftui/accessibilityheadinglevel) — 某个标题相对于其他标题的层级。
- [AccessibilityTextContentType](https://developer.apple.com/documentation/swiftui/accessibilitytextcontenttype) — 辅助技术可用来改善朗读文本呈现效果的文本上下文。

## 描述图表 {#Describing-charts}

- [accessibilityChartDescriptor(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilitychartdescriptor(_:)) — 为一个表示图表的 View 添加描述符，让图表的内容对所有用户都可访问。
- [AXChartDescriptorRepresentable](https://developer.apple.com/documentation/swiftui/axchartdescriptorrepresentable) — 用于生成 `AXChartDescriptor` 对象的类型，你用它为 VoiceOver 等辅助技术提供关于图表及其数据的可访问体验。

## 添加自定义描述 {#Adding-custom-descriptions}

- [accessibilityCustomContent(_:_:importance:)](https://developer.apple.com/documentation/swiftui/view/accessibilitycustomcontent(_:_:importance:)) — 为视图添加额外的辅助功能信息。
- [AccessibilityCustomContentKey](https://developer.apple.com/documentation/swiftui/accessibilitycustomcontentkey) — 用于指定附加辅助功能信息条目所关联标识符和标签的键。

## 为内容分配特征 {#Assigning-traits-to-content}

- [accessibilityAddTraits(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityaddtraits(_:)) — 为视图添加给定的特征。
- [accessibilityRemoveTraits(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityremovetraits(_:)) — 从该视图移除给定的特征。
- [AccessibilityTraits](https://developer.apple.com/documentation/swiftui/accessibilitytraits) — 一组描述元素行为的辅助功能特征。

## 提供提示 {#Offering-hints}

- [accessibilityHint(_:)](https://developer.apple.com/documentation/swiftui/view/accessibilityhint(_:)) — 告知用户执行该视图的动作之后会发生什么。
- [accessibilityHint(_:isEnabled:)](https://developer.apple.com/documentation/swiftui/view/accessibilityhint(_:isenabled:)) — 告知用户执行该视图的动作之后会发生什么。

## 配置 VoiceOver {#Configuring-VoiceOver}

- [speechAdjustedPitch(_:)](https://developer.apple.com/documentation/swiftui/view/speechadjustedpitch(_:)) — 提高或降低朗读文本的音高。
- [speechAlwaysIncludesPunctuation(_:)](https://developer.apple.com/documentation/swiftui/view/speechalwaysincludespunctuation(_:)) — 设置 VoiceOver 是否应始终读出文本视图中的所有标点符号。
- [speechAnnouncementsQueued(_:)](https://developer.apple.com/documentation/swiftui/view/speechannouncementsqueued(_:)) — 控制待播报内容是排在已有朗读内容之后，而不是打断正在进行的朗读。
- [speechSpellsOutCharacters(_:)](https://developer.apple.com/documentation/swiftui/view/speechspellsoutcharacters(_:)) — 设置 VoiceOver 是否应逐字符读出文本视图的内容。
