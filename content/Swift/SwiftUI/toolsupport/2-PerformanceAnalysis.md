+++
title = "2 性能分析"
date = 2026-09-12T12:47:47+08:00
weight = 2
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/performance-analysis](https://developer.apple.com/documentation/swiftui/performance-analysis)

# 2 性能分析

测量并改善应用的响应能力。

## 概述 {#Overview}

使用 Instruments 检测应用中的卡死（hang）和卡顿（hitch），并分析可能造成卡死和卡顿的长时间视图 body 更新以及频繁发生的 SwiftUI 更新。

## 基础 {#Essentials}

- [理解用户界面的响应能力](https://developer.apple.com/documentation/xcode/understanding-user-interface-responsiveness) — 通过检查事件处理与渲染循环，让你的应用响应更快。
- [理解应用中的卡死](https://developer.apple.com/documentation/xcode/understanding-hangs-in-your-app) — 通过检查主线程和主运行循环，确定用户交互延迟的原因。
- [理解应用中的卡顿](https://developer.apple.com/documentation/xcode/understanding-hitches-in-your-app) — 通过检查渲染循环，确定动态画面中断的原因。

## 分析 SwiftUI 性能 {#Analyzing-SwiftUI-performance}

- [理解并改善 SwiftUI 性能](https://developer.apple.com/documentation/xcode/understanding-and-improving-swiftui-performance) — 找出并解决耗时较长的视图更新，并降低更新频率。
