+++
title = "2 视图配置"
date = 2026-09-12T12:47:47+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/view-configuration](https://developer.apple.com/documentation/swiftui/view-configuration)

# 2 视图配置

调整层级中各视图的特征。

## 概述 {#Overview}

SwiftUI 让你可以用视图修饰符调节视图的外观与行为。

![](./images/view-configuration-hero@2x.png)

许多修饰符只作用于特定种类的视图或行为，但有些修饰符更为通用。例如，你可以通过动态设置不透明度来有条件地隐藏任何视图，在人们把指针悬停在视图上时显示上下文帮助，或者为视图请求浅色或深色外观。

## 隐藏视图 {#Hiding-views}

- [opacity(_:)](https://developer.apple.com/documentation/swiftui/view/opacity(_:)) —— 设置该视图的透明度。
- [hidden()](https://developer.apple.com/documentation/swiftui/view/hidden()) —— 无条件隐藏该视图。

## 隐藏系统元素 {#Hiding-system-elements}

- [labelsHidden()](https://developer.apple.com/documentation/swiftui/view/labelshidden()) —— 隐藏该视图内任何控件的标签。
- [labelsVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/labelsvisibility(_:)) —— 控制该视图内任何控件标签的可见性。
- [labelsVisibility](https://developer.apple.com/documentation/swiftui/environmentvalues/labelsvisibility) —— 由 [labelsVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/labelsvisibility(_:)) 设置的标签可见性。
- [menuIndicator(_:)](https://developer.apple.com/documentation/swiftui/view/menuindicator(_:)) —— 设置该视图内控件的菜单指示器可见性。
- [statusBarHidden(_:)](https://developer.apple.com/documentation/swiftui/view/statusbarhidden(_:)) —— 设置状态栏的可见性。
- [persistentSystemOverlays(_:)](https://developer.apple.com/documentation/swiftui/view/persistentsystemoverlays(_:)) —— 设置覆盖在应用之上、非瞬态系统视图的偏好可见性。
- [Visibility](https://developer.apple.com/documentation/swiftui/visibility) —— UI 元素的可见性，依据平台、当前上下文和其他因素自动选择。

## 管理视图交互 {#Managing-view-interaction}

- [disabled(_:)](https://developer.apple.com/documentation/swiftui/view/disabled(_:)) —— 添加一个条件，控制用户能否与该视图交互。
- [isEnabled](https://developer.apple.com/documentation/swiftui/environmentvalues/isenabled) —— 表示与该环境关联的视图是否允许用户交互的布尔值。
- [interactionActivityTrackingTag(_:)](https://developer.apple.com/documentation/swiftui/view/interactionactivitytrackingtag(_:)) —— 设置用于跟踪交互性的标签。
- [invalidatableContent(_:)](https://developer.apple.com/documentation/swiftui/view/invalidatablecontent(_:)) —— 把接收者标记为其内容可能失效。

## 提供上下文帮助 {#Providing-contextual-help}

- [help(_:)](https://developer.apple.com/documentation/swiftui/view/help(_:)) —— 用你提供的本地化字符串资源为视图添加帮助文本。

## 检测并请求浅色或深色外观 {#Detecting-and-requesting-the-light-or-dark-appearance}

- [preferredColorScheme(_:)](https://developer.apple.com/documentation/swiftui/view/preferredcolorscheme(_:)) —— 为该呈现设置偏好的配色方案。
- [colorScheme](https://developer.apple.com/documentation/swiftui/environmentvalues/colorscheme) —— 该环境的配色方案。
- [ColorScheme](https://developer.apple.com/documentation/swiftui/colorscheme) —— 可能的配色方案，对应浅色和深色外观。

## 获取配色方案对比度 {#Getting-the-color-scheme-contrast}

- [colorSchemeContrast](https://developer.apple.com/documentation/swiftui/environmentvalues/colorschemecontrast) —— 与该环境配色方案关联的对比度。
- [ColorSchemeContrast](https://developer.apple.com/documentation/swiftui/colorschemecontrast) —— 应用前景色与背景色之间的对比度。

## 配置透视画面 {#Configuring-passthrough}

- [preferredSurroundingsEffect(_:)](https://developer.apple.com/documentation/swiftui/view/preferredsurroundingseffect(_:)) —— 对透视视频应用一种效果。
- [SurroundingsEffect](https://developer.apple.com/documentation/swiftui/surroundingseffect) —— 系统可以应用到透视视频上的效果。
- [breakthroughEffect(_:)](https://developer.apple.com/documentation/swiftui/view/breakthrougheffect(_:)) —— 确保该视图始终对用户可见，即使像 3D 模型这样的其他内容遮挡了它。
- [BreakthroughEffect](https://developer.apple.com/documentation/swiftui/breakthrougheffect)

## 屏蔽私密内容 {#Redacting-private-content}

- [为「始终显示」状态设计你的应用](https://developer.apple.com/documentation/watchos-apps/designing-your-app-for-the-always-on-state) —— 为持续显示定制你的 watchOS 应用界面。
- [在屏幕共享与远程控制启用时保护敏感内容](2.1-ProtectingSensitiveContentWhenScreenSharing/) —— 检测正在进行的屏幕录制会话，并做出恰当响应，保护应用中的敏感内容。
- [privacySensitive(_:)](https://developer.apple.com/documentation/swiftui/view/privacysensitive(_:)) —— 把该视图标记为包含敏感的私密用户数据。
- [redacted(reason:)](https://developer.apple.com/documentation/swiftui/view/redacted(reason:)) —— 添加一个理由，对该视图层级应用屏蔽。
- [unredacted()](https://developer.apple.com/documentation/swiftui/view/unredacted()) —— 移除对该视图层级应用屏蔽的任何理由。
- [redactionReasons](https://developer.apple.com/documentation/swiftui/environmentvalues/redactionreasons) —— 当前应用于视图层级的屏蔽理由。
- [isSceneCaptured](https://developer.apple.com/documentation/swiftui/environmentvalues/isscenecaptured) —— 当前的捕获状态。
- [RedactionReasons](https://developer.apple.com/documentation/swiftui/redactionreasons) —— 对屏幕上显示的数据应用屏蔽的理由。
