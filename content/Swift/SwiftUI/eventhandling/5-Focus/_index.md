+++
title = "5 焦点"
date = 2026-09-12T12:47:47+08:00
weight = 5
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/focus](https://developer.apple.com/documentation/swiftui/focus)

# 5 焦点

识别并控制哪个可见对象响应用户交互。

## 概述 {#Overview}

焦点指示显示区域中的哪个元素接收下一次输入。使用视图修饰符可以指明哪些视图能够接收焦点、检测哪个视图拥有焦点，并以编程方式控制焦点状态。

![](./images/focus-hero@2x.png)

关于设计指导，请参阅 Human Interface Guidelines 中的 [焦点与选择](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection)。

## 基础 {#Essentials}

- [焦点手册：在 SwiftUI 应用中支持并增强由焦点驱动的交互](5.1-FocusCookbookSample/) — 创建带按键处理器的自定义可聚焦视图，从而加快键盘输入并支持移动操作，同时以编程方式控制焦点。

## 指明视图可以接收焦点 {#Indicating-that-a-view-can-receive-focus}

- [focusable(_:)](https://developer.apple.com/documentation/swiftui/view/focusable(_:)) — 指明该视图是否可聚焦。
- [focusable(_:interactions:)](https://developer.apple.com/documentation/swiftui/view/focusable(_:interactions:)) — 指明该视图是否可聚焦，若可聚焦，还指明它支持哪些由焦点驱动的交互。
- [FocusInteractions](https://developer.apple.com/documentation/swiftui/focusinteractions) — 这些值描述视图可以支持的不同焦点交互。

## 管理焦点状态 {#Managing-focus-state}

- [focused(_:equals:)](https://developer.apple.com/documentation/swiftui/view/focused(_:equals:)) — 把视图的焦点状态绑定到给定的状态值，从而修改这个视图。
- [focused(_:)](https://developer.apple.com/documentation/swiftui/view/focused(_:)) — 把视图的焦点状态绑定到给定的布尔状态值，从而修改这个视图。
- [isFocused](https://developer.apple.com/documentation/swiftui/environmentvalues/isfocused) — 返回最近的可聚焦祖先视图是否拥有焦点。
- [FocusState](https://developer.apple.com/documentation/swiftui/focusstate) — 一种属性包装器类型，可以读写一个由 SwiftUI 在场景内焦点位置变化时更新的值。
- [FocusedValue](https://developer.apple.com/documentation/swiftui/focusedvalue) — 一种属性包装器，用于从获得焦点的视图或其某个祖先视图观察值。
- [Entry()](https://developer.apple.com/documentation/swiftui/entry()) — 创建一个环境值、事务、容器值或焦点值条目。
- [FocusedValueKey](https://developer.apple.com/documentation/swiftui/focusedvaluekey) — 发布和观察焦点值时所用标识符类型的协议。
- [FocusedBinding](https://developer.apple.com/documentation/swiftui/focusedbinding) — 一种便捷的属性包装器，用于从获得焦点的视图或其某个祖先视图观察并自动解包状态绑定。
- [searchFocused(_:)](https://developer.apple.com/documentation/swiftui/view/searchfocused(_:)) — 把与最近的 searchable 修饰符关联的搜索框的焦点状态绑定到给定的布尔值，从而修改这个视图。
- [searchFocused(_:equals:)](https://developer.apple.com/documentation/swiftui/view/searchfocused(_:equals:)) — 把与最近的 searchable 修饰符关联的搜索框的焦点状态绑定到给定的值，从而修改这个视图。

## 向获得焦点的视图暴露值类型 {#Exposing-value-types-to-focused-views}

- [focusedValue(_:)](https://developer.apple.com/documentation/swiftui/view/focusedvalue(_:)) — 为给定的对象类型设置焦点值。
- [focusedValue(_:_:)](https://developer.apple.com/documentation/swiftui/view/focusedvalue(_:_:)) — 注入一个你提供的值，供其他状态取决于焦点视图层级的视图使用，从而修改这个视图。
- [focusedSceneValue(_:)](https://developer.apple.com/documentation/swiftui/view/focusedscenevalue(_:)) — 在场景范围内为给定的对象类型设置焦点值。
- [focusedSceneValue(_:_:)](https://developer.apple.com/documentation/swiftui/view/focusedscenevalue(_:_:)) — 注入一个你提供的值，供其他状态取决于获得焦点场景的视图使用，从而修改这个视图。
- [FocusedValues](https://developer.apple.com/documentation/swiftui/focusedvalues) — 由获得焦点的场景或视图及其祖先视图导出的一组状态。

## 向获得焦点的视图暴露引用类型 {#Exposing-reference-types-to-focused-views}

- [focusedObject(_:)](https://developer.apple.com/documentation/swiftui/view/focusedobject(_:)) — 创建一个新视图，把提供的对象暴露给其他状态取决于焦点视图层级的视图。
- [focusedSceneObject(_:)](https://developer.apple.com/documentation/swiftui/view/focusedsceneobject(_:)) — 创建一个新视图，把提供的对象暴露给其他状态取决于活跃场景的视图。
- [FocusedObject](https://developer.apple.com/documentation/swiftui/focusedobject) — 一种属性包装器类型，用于表示由获得焦点的视图或其某个祖先视图提供的可观察对象。

## 设置焦点范围 {#Setting-focus-scope}

- [focusScope(_:)](https://developer.apple.com/documentation/swiftui/view/focusscope(_:)) — 创建一个焦点范围，SwiftUI 用它来限制默认焦点偏好。
- [focusSection()](https://developer.apple.com/documentation/swiftui/view/focussection()) — 指明应使用该视图的框架及其可聚焦后代群体来引导焦点移动。

## 控制默认焦点 {#Controlling-default-focus}

- [prefersDefaultFocus(_:in:)](https://developer.apple.com/documentation/swiftui/view/prefersdefaultfocus(_:in:)) — 指明在给定命名空间中该视图应默认接收焦点。
- [defaultFocus(_:_:priority:)](https://developer.apple.com/documentation/swiftui/view/defaultfocus(_:_:priority:)) — 通过给给定的焦点状态绑定赋值，定义窗口中评估默认焦点的区域。
- [DefaultFocusEvaluationPriority](https://developer.apple.com/documentation/swiftui/defaultfocusevaluationpriority) — 在不同情形下评估焦点的移动位置时，默认焦点偏好的优先级。

## 重置焦点 {#Resetting-focus}

- [resetFocus](https://developer.apple.com/documentation/swiftui/environmentvalues/resetfocus) — 一个请求焦点系统重新评估默认焦点的动作。
- [ResetFocusAction](https://developer.apple.com/documentation/swiftui/resetfocusaction) — 一个环境值，提供重新评估默认焦点的能力。

## 配置效果 {#Configuring-effects}

- [focusEffectDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/focuseffectdisabled(_:)) — 添加一个条件，控制该视图是否可以显示焦点效果，例如默认的焦点环或悬停效果。
- [isFocusEffectEnabled](https://developer.apple.com/documentation/swiftui/environmentvalues/isfocuseffectenabled) — 一个布尔值，指示与该环境关联的视图是否允许显示焦点效果。
